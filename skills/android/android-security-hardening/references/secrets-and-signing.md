# Secrets & signing — reference

## 1. The rule
There is **no such thing as a secret inside an APK**. Anything shipped to a device is public.
Therefore:

| Secret | Where it belongs |
|---|---|
| Upload/signing keystore | GitHub Secrets (base64) + an offline encrypted backup |
| Play service-account JSON | GitHub Secrets, used only by the publish job |
| Backend API credentials | Your server, never the app |
| Third-party API key that must reach the device (e.g. Maps) | Restricted by package name + SHA-1 fingerprint in the vendor console, and treated as public |
| Crash reporter DSN | Public by nature; restrict server-side |

## 2. Keystore lifecycle

```bash
keytool -genkeypair -v \
  -keystore upload-keystore.jks -alias upload \
  -keyalg RSA -keysize 4096 -validity 10000 \
  -storetype PKCS12
```
- **Play App Signing** is mandatory for new apps: Google holds the *app signing key*; you hold the
  *upload key*. If you lose the upload key you can request a reset — if you were not enrolled and
  lose the app signing key, the app is unrecoverable.
- Store the keystore + passwords in a password manager **and** an encrypted offline backup in a
  second physical location.
- Rotate the upload key only through the Play Console reset flow.
- Never commit `*.jks`, `keystore.properties`, or `google-play-service-account.json`.

## 3. CI signing (GitHub Actions)

```yaml
- name: Decode keystore
  env:
    KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
  run: |
    echo "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/upload.jks"
    echo "KEYSTORE_PATH=$RUNNER_TEMP/upload.jks" >> "$GITHUB_ENV"

- name: Build signed bundle
  env:
    KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
  run: ./gradlew bundleRelease

- name: Shred keystore
  if: always()
  run: rm -f "$RUNNER_TEMP/upload.jks"
```
Read them in Gradle with `providers.environmentVariable(...)` so the configuration cache still works.

## 4. Preventing accidental leaks
- Add a secret scanner to CI: `gitleaks detect --no-banner --redact`.
- Enable GitHub **push protection** and secret scanning on the repository.
- `.gitignore`: `*.jks`, `*.keystore`, `keystore.properties`, `local.properties`, `*.p12`, `*service-account*.json`.
- Pre-commit hook rejecting `-----BEGIN` and `AIza[0-9A-Za-z_-]{35}` patterns.
- If a key leaks: revoke first, rotate, then rewrite history — in that order.

## 5. Runtime configuration instead of baked secrets
- Fetch feature flags and endpoints from a config service (Remote Config) over TLS.
- Device-to-backend auth: sign in the user → server issues a short-lived JWT → app stores it in the Keystore.
- For unauthenticated APIs that must not be abused, use **Play Integrity** attestation verified on
  your server before issuing a token.

## 6. Verifying what shipped
```bash
# What signed this artifact?
apksigner verify --print-certs app-release.apk
# Confirm no secrets survived
unzip -p app-release.apk classes.dex | strings | grep -Ei "secret|api_key|password"
# Confirm the release is not debuggable
apkanalyzer manifest debuggable app-release.apk   # expect false
```

## 7. Incident checklist (leaked key or credential)
1. Revoke/rotate the credential at the provider **immediately**.
2. Invalidate issued tokens/sessions.
3. Ship an app update if the leak is exploitable client-side.
4. Purge the secret from git history (`git filter-repo`) and force-push with team coordination.
5. Post-mortem: how did it bypass the scanner? Add the missing rule.

# MASVS audit checklist — reference

Mapped to OWASP MASVS v2 control groups. Mark each item Pass / Fail / N-A with evidence.

## MASVS-STORAGE — data at rest
- [ ] No sensitive data in plain `SharedPreferences`, unencrypted DB, or files.
- [ ] Keys generated in the Android Keystore (`setUserAuthenticationRequired` for high value; StrongBox where available).
- [ ] No sensitive data written to external storage or app cache.
- [ ] No sensitive data in logs (`Log.*`, Timber release tree drops verbose).
- [ ] `allowBackup=false` or `dataExtractionRules` excludes secrets (both cloud and device-to-device).
- [ ] Keyboard cache disabled for secret fields (`inputType="textNoSuggestions|textPassword"`).
- [ ] Sensitive screens set `FLAG_SECURE` (blocks screenshots and recents preview).
- [ ] Clipboard: sensitive copy marked `EXTRA_IS_SENSITIVE`.
- [ ] All sensitive data wiped on logout/uninstall path.

## MASVS-CRYPTO
- [ ] Only vetted primitives: AES-256-GCM, RSA-OAEP/ECDSA P-256, SHA-256+, Argon2/PBKDF2 for passwords.
- [ ] No ECB, no hardcoded IV/salt, no MD5/SHA-1 for security purposes.
- [ ] `SecureRandom` for all key/nonce/token generation.
- [ ] Keys never leave the Keystore; no key material in memory longer than needed.
- [ ] Crypto agility: algorithm/version stored with the ciphertext for future migration.

## MASVS-AUTH
- [ ] Server enforces every authorisation decision; client checks are UX only.
- [ ] Access tokens short-lived; refresh tokens rotated and revocable.
- [ ] Biometric prompt uses `BiometricPrompt` with a `CryptoObject` (not a boolean callback).
- [ ] Fallback path (device credential) is as strong as the primary.
- [ ] Session invalidated server-side on logout and on password change.
- [ ] Brute-force protection and account lockout are server-side.

## MASVS-NETWORK
- [ ] TLS 1.2+ enforced; `cleartextTrafficPermitted="false"` in release.
- [ ] Certificate/public-key pinning with **two** pins and a documented expiry (`expiration` attribute).
- [ ] No custom `TrustManager`/`HostnameVerifier` bypasses; debug overrides scoped to debug builds.
- [ ] Server certificate errors are fatal — never "continue anyway".
- [ ] Request/response logging disabled in release.

## MASVS-PLATFORM
- [ ] Every `<activity>/<service>/<receiver>/<provider>` has an explicit `android:exported`.
- [ ] Exported components validate the caller (signature permission or `getCallingUid` check).
- [ ] `PendingIntent` uses `FLAG_IMMUTABLE` (or a justified `FLAG_MUTABLE`) and an explicit intent.
- [ ] No `UnsafeIntentLaunch`: never `startActivity(intent.getParcelableExtra(...))`.
- [ ] `ContentProvider` uses `grantUriPermissions` narrowly; `FileProvider` paths are minimal.
- [ ] WebView: JavaScript off unless required; `addJavascriptInterface` avoided; `setAllowFileAccess(false)`, `setAllowUniversalAccessFromFileURLs(false)`; URL allowlist in `shouldOverrideUrlLoading`.
- [ ] Deep links verified (App Links + `assetlinks.json`), all parameters validated.
- [ ] Permissions minimal; no `QUERY_ALL_PACKAGES`, no legacy storage permission.
- [ ] `taskAffinity`/`launchMode` reviewed against StrandHogg-style task hijacking.

## MASVS-CODE
- [ ] Release is not debuggable and not `testOnly`.
- [ ] R8 obfuscation + optimization enabled; mapping archived.
- [ ] All dependencies scanned (OSV/dependency-check); no known high/critical CVEs.
- [ ] Native libs compiled with stack protector/PIE; no debug symbols shipped in the APK.
- [ ] Input validation on all external data; SQL always parameterised (Room does this).
- [ ] Error messages reveal nothing about the backend internals.
- [ ] `BuildConfig.DEBUG` guards every dev backdoor; no hidden debug menus in release.

## MASVS-RESILIENCE (only if the threat model demands it)
- [ ] Play Integrity API verdict verified **server-side**.
- [ ] Root/emulator/debugger detection as telemetry, not as a hard gate.
- [ ] Tamper detection: verify the signing certificate at runtime, respond by degrading gracefully.
- [ ] No security control depends solely on client-side enforcement.

## MASVS-PRIVACY
- [ ] Data inventory documented (what, why, where, retention, third parties).
- [ ] Play Data safety declaration matches reality, including SDK-collected data.
- [ ] Privacy policy URL live and accurate; in-app consent before any analytics.
- [ ] Advertising ID used only with the declared purpose and the `AD_ID` permission.
- [ ] Account deletion available in-app **and** via a web URL (Play requirement).
- [ ] Data minimisation: no field collected "just in case".
- [ ] Children's policy / Families programme requirements checked if applicable.

## Tooling
```bash
# Static analysis
docker run -p 8000:8000 opensecurity/mobile-security-framework-mobsf   # MobSF

# Inspect the merged manifest & strings
apkanalyzer manifest print app-release.apk
strings app-release.apk | grep -Ei "api[_-]?key|secret|password|BEGIN (RSA|EC) PRIVATE"

# Dependency vulnerabilities
./gradlew dependencyCheckAnalyze          # OWASP dependency-check
osv-scanner --lockfile gradle.lockfile

# Runtime traffic inspection (debug build only)
mitmproxy   # verify pinning actually blocks interception in release
```

## Evidence pack to archive per release
1. Completed checklist with dates and owner.
2. MobSF report PDF.
3. Dependency scan output.
4. Manifest dump of the release AAB.
5. Confirmation that pinning blocks a MITM proxy on the release build.

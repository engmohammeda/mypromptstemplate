---
name: android-security-hardening
description: >-
  Hardens Android apps against the OWASP Mobile Top 10 and MASVS: secure storage and keystore,
  network TLS and certificate pinning, secrets handling, component exposure, WebView safety,
  deep-link validation, obfuscation, root/tamper checks, and privacy/Data safety compliance.
  Use when the user mentions security, encryption, EncryptedSharedPreferences, Keystore, API keys,
  secrets, certificate pinning, OWASP, MASVS, pentest, exported components, WebView, deep links,
  biometrics, permissions, or asks whether an Android app is safe to ship.
version: 1.0.0
license: MIT
category: android
tags: [android, security, owasp, masvs, keystore, tls, privacy, hardening]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "تحصين تطبيقات أندرويد وفق OWASP MASVS: التخزين الآمن، الشبكة، الأسرار، المكوّنات المكشوفة، والخصوصية."
---

# Android Security Hardening

You are the application security engineer. You assume the device is **rooted, the network is
hostile, and the APK will be decompiled**.

## When to use
- Any app handling auth, payments, personal data, or health data.
- Pre-release security review; responding to a pentest or a Play policy rejection.

## When NOT to use
- General code quality → `android-testing-quality`.
- Store metadata/Data safety form filling → `android-play-release` (but the data inventory comes from here).

## Non-negotiables
- **MUST** assume every string in the APK is public. **NEVER** store API secrets, private keys, or admin tokens in the app — not in `BuildConfig`, `strings.xml`, `local.properties`, NDK, nor obfuscated.
- **MUST** use HTTPS only. `cleartextTrafficPermitted="false"` in the Network Security Config; no exceptions in release.
- **MUST** store tokens/credentials in `EncryptedSharedPreferences`/`DataStore` backed by the **Android Keystore**, or better, never persist them at all.
- **MUST** set `android:exported` explicitly on every component and keep it `false` unless there is a documented reason; protect exported components with signature permissions.
- **MUST** validate every deep link / intent extra as untrusted input; **NEVER** launch an `Intent` parsed from external data (`UnsafeIntentLaunch`).
- **MUST** set `android:allowBackup="false"` (or a strict `dataExtractionRules`) for apps with sensitive data.
- **MUST** enable R8 obfuscation for release; **NEVER** ship a debuggable release (`android:debuggable="true"`).
- **NEVER** disable certificate validation, use `TrustAllX509TrustManager`, or a custom `HostnameVerifier` returning `true`.
- **NEVER** log PII, tokens, or full request/response bodies in release (`OkHttp` logging interceptor must be debug-only).
- **NEVER** enable `setJavaScriptEnabled(true)` on a WebView loading remote content without a strict allowlist and `addJavascriptInterface` avoided entirely.
- **MUST** request the minimum permissions, at the moment of need, with a rationale.

## Version pins
| Component | Version |
|---|---|
| OWASP MASVS | v2.x |
| security-crypto | 1.1.x (AndroidX) |
| OkHttp (pinning) | 5.x |
| Play Integrity API | latest |
| minSdk for Keystore StrongBox | 28+ |

## Workflow
1. **Inventory the data**: what is collected, why, where it goes, retention. This feeds the Play Data safety form and the privacy policy.
2. **Threat model** (STRIDE-lite): attacker on the network, on the device, malicious app on the same device, malicious server response.
3. **Fix storage**: encrypt at rest, use the Keystore, no sensitive data in logs/cache/screenshots (`FLAG_SECURE` for sensitive screens).
4. **Fix transport**: Network Security Config, TLS 1.2+, consider certificate pinning with a backup pin and an expiry plan.
5. **Fix components**: audit the merged manifest for exported activities/services/receivers/providers.
6. **Fix input**: deep links, intents, `ContentProvider` URIs, WebView `shouldOverrideUrlLoading`, file paths (path traversal), SQL (parameterised queries only).
7. **Fix auth**: short-lived tokens, refresh rotation, biometric prompt with `CryptoObject` for high-value actions, logout wipes the keystore alias.
8. **Add integrity signals**: Play Integrity API for server-side verification (never trust a client-side root check alone).
9. **Scan**: MobSF static scan, `dependency-check`/OSV for vulnerable libraries, Android Lint security checks, secret scanning in CI.
10. **Document** residual risks and mitigations in `docs/security-review.md`.

## Patterns

✅ **Network Security Config (`res/xml/network_security_config.xml`)**
```xml
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors><certificates src="system" /></trust-anchors>
    </base-config>
    <domain-config>
        <domain includeSubdomains="true">api.company.com</domain>
        <pin-set expiration="2027-06-01">
            <pin digest="SHA-256">base64PrimaryPin=</pin>
            <pin digest="SHA-256">base64BackupPin=</pin>
        </pin-set>
    </domain-config>
    <debug-overrides>
        <trust-anchors><certificates src="user" /></trust-anchors>   <!-- debug builds only -->
    </debug-overrides>
</network-security-config>
```

✅ **Encrypted storage**
```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .setUserAuthenticationRequired(false)
    .build()

val prefs = EncryptedSharedPreferences.create(
    context, "auth", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
)
```

✅ **Secrets stay out of the repo**
```kotlin
// build.gradle.kts — value comes from CI secrets / local.properties (git-ignored)
buildConfigField("String", "API_BASE_URL", "\"${providers.gradleProperty("apiBaseUrl").get()}\"")
```
Real secrets (signing keys, service accounts) live in **GitHub Secrets**; app-to-backend auth uses
short-lived tokens issued by your server, never a baked-in key.

✅ **Safe deep link handling**
```kotlin
val id = intent.data?.getQueryParameter("id")
    ?.takeIf { it.matches(Regex("^[a-zA-Z0-9_-]{1,36}$")) }
    ?: return finish()
```
Use App Links with `android:autoVerify="true"` and a hosted `assetlinks.json`.

❌ **Don't**
```kotlin
const val API_KEY = "sk_live_9f3a..."                     // extractable in 30 seconds
OkHttpClient.Builder().hostnameVerifier { _, _ -> true }  // MITM by design
webView.settings.javaScriptEnabled = true
webView.addJavascriptInterface(AppBridge(), "Android")    // remote JS → native RCE
Log.d("Auth", "token=$accessToken")                       // leaks to logcat/crash reports
```

## Anti-patterns
- Client-side-only authorisation ("hide the admin button") — the server must enforce it.
- Root detection / SSL-pinning treated as a security boundary rather than a speed bump.
- Rolling your own crypto, ECB mode, static IVs, `Random` instead of `SecureRandom`.
- Hardcoded pins with no backup pin and no expiry → app-wide outage when the cert rotates.
- `WRITE_EXTERNAL_STORAGE` or `QUERY_ALL_PACKAGES` "for convenience" → Play policy rejection.
- Sensitive data in `onSaveInstanceState`, screenshots, or the recents thumbnail.
- Vulnerable transitive dependencies never scanned.

## Definition of Done
- [ ] No secrets in the repo or the APK (verified with `strings`/APK Analyzer + a secret scanner).
- [ ] Cleartext traffic disabled; TLS 1.2+; pinning (if used) has a backup pin and rotation plan.
- [ ] All tokens encrypted at rest; wiped on logout.
- [ ] Merged manifest audited: no unintentionally exported components; `allowBackup` decided.
- [ ] All external input (deep links, intents, provider URIs, WebView URLs) validated.
- [ ] Release build: not debuggable, obfuscated, no verbose logging.
- [ ] Permissions minimal and justified; runtime rationale implemented.
- [ ] Dependency vulnerability scan clean (no known high/critical).
- [ ] MASVS checklist (`references/masvs-checklist.md`) completed and archived.
- [ ] Play Data safety form matches the actual data inventory.

## References
- `references/masvs-checklist.md` — the full audit checklist mapped to OWASP MASVS/MASTG.
- `references/secrets-and-signing.md` — key management, CI signing, keystore lifecycle.
- OWASP MASVS: https://mas.owasp.org/MASVS/
- Android security best practices: https://developer.android.com/privacy-and-security/security-tips

## ملخص عربي
افترض أن الجهاز مخترق والشبكة معادية والتطبيق سيُفكَّك. لا تضع أي سر داخل التطبيق إطلاقًا، وشفّر
كل بيانات الاعتماد عبر Android Keystore، وامنع الاتصال غير المشفّر، وحدّد `exported` لكل مكوّن،
وتعامل مع كل رابط عميق أو intent كمدخل غير موثوق. الإصدار النهائي: مبهم، غير قابل للتصحيح، بلا
سجلات حساسة. أنهِ المراجعة بقائمة MASVS كاملة وفحص للثغرات في المكتبات.

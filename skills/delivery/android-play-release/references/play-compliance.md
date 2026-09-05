# Play compliance checklist — reference

Run this **before** building the release candidate.

## 1. Technical requirements
- [ ] `targetSdk` = current requirement (API 36 for phones/tablets since 2026-08-31; Wear/Automotive 35; TV/XR 34).
- [ ] 64-bit native libraries present for every 32-bit lib.
- [ ] Uploading an **AAB**; base module ≤ 200 MB.
- [ ] Play App Signing enrolled; upload key backed up.
- [ ] `versionCode` strictly greater than every previously uploaded code (including rolled-back ones).
- [ ] Release build not debuggable, `testOnly` absent, obfuscated.
- [ ] Mapping file + native debug symbols uploaded.
- [ ] App supports both light and dark themes without unreadable screens.
- [ ] Edge-to-edge handled (API 35+) — no content under the system bars.
- [ ] Predictive back supported on API 36 (`enableOnBackInvokedCallback`).
- [ ] Large-screen quality: no orientation lock, no letterboxing, works in split-screen.

## 2. Declarations (the top source of rejections)
- [ ] **Data safety**: every data type collected/shared, including by third-party SDKs, with purpose,
      encryption-in-transit and deletion-request statements. Audit each SDK's own disclosure.
- [ ] **Content rating** questionnaire re-taken if the content changed.
- [ ] **Ads** declaration matches reality; ad SDKs disclosed; `AD_ID` permission declared if used.
- [ ] **Target audience & content**: if children are targeted, the Families policy applies (ad SDK allowlist, no ad ID for under-13).
- [ ] **Government apps / financial features / health** declarations if applicable.
- [ ] **Permissions declaration form** for any sensitive permission (all-files access, SMS/Call Log,
      accessibility, exact alarms, package visibility, foreground location, camera/mic background).
- [ ] Privacy policy URL live, reachable, in the listing **and** in-app.
- [ ] Account deletion: in-app path + a public web URL that works without installing the app.

## 3. Policy self-review
| Area | Ask yourself |
|---|---|
| Deceptive behaviour | Does the app do exactly what the listing claims? Any hidden functionality? |
| User data | Is every collection disclosed and necessary? Prominent disclosure + consent for sensitive data? |
| Permissions | Is each permission used by a core, user-visible feature? |
| Device abuse | Any background behaviour that drains battery, self-updates code, or downloads executables? |
| Impersonation | Does the icon/name/branding resemble another app or a brand you don't own? |
| Restricted content | UGC without reporting/moderation? Gambling, health claims, crypto, loans? |
| Subscriptions | Price, period, trial and cancellation clearly stated before purchase? Play Billing used for digital goods? |
| Intellectual property | All fonts, icons, images, sounds licensed for commercial use? |
| Spam | Keyword-stuffed title/description? Duplicate app of an existing listing? |

## 4. Account & organisational requirements
- [ ] Developer identity verification complete (required from 2026-09-30, phased by country) — for
      Play distribution **and** for apps distributed outside Play under the developer-verification programme.
- [ ] New personal developer accounts: closed test with ≥ 20 testers running ≥ 14 continuous days before production access.
- [ ] Correct account type (organisation accounts need a D-U-N-S number).
- [ ] Contact email and physical address published as required.

## 5. Testing evidence before submitting
- [ ] Installed the exact internal-track artifact on: one low-end device (2 GB RAM, API 28ish),
      one current mid-range, one tablet or foldable.
- [ ] Smoke script passed: install → onboarding → login → core flow → logout → uninstall → reinstall.
- [ ] Upgrade path tested: previous production version installed, then updated — data intact, no crash.
- [ ] Offline behaviour verified.
- [ ] Deep links and notification taps open the right screens from a cold start.
- [ ] Pre-launch report: zero crashes, no critical accessibility/security findings.
- [ ] Localisation spot-checked in each shipped language, including RTL layouts for Arabic.

## 6. Common rejection reasons and the fix

| Rejection | Fix |
|---|---|
| Data safety mismatch | Re-audit SDKs (`./gradlew :app:dependencies`), update the form, resubmit |
| Broken functionality found by review | Ensure demo credentials are provided in "App access" for gated apps |
| Missing privacy policy | Host a real policy; a placeholder page is rejected |
| Permissions not justified | Remove, or file the declaration with a video demo |
| Metadata policy | Remove pricing/promo/emoji/keyword stuffing from title and short description |
| Impersonation/IP | Change icon/name; hold rights to all brand assets |
| Background location | Provide the required prominent disclosure and a video |
| Target API too low | Bump `targetSdk`, fix behaviour changes, rebuild |
| Crash on review devices | Read the pre-launch report; test on the exact API level reviewers used |

## 7. If rejected or suspended
1. Read the exact policy clause cited — do not guess.
2. Fix the root cause; document what changed.
3. Reply through the Policy status page with evidence (screenshots, video, code diff).
4. Appeals: one clear submission beats several partial ones.
5. Repeated violations put the whole developer account at risk — treat the first warning as critical.

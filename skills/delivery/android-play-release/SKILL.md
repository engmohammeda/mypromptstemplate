---
name: android-play-release
description: >-
  Prepares and ships Android releases to Google Play: target API compliance, app signing, versioning,
  release tracks and staged rollout, store listing and ASO assets, Data safety and privacy
  declarations, policy pre-checks, pre-launch reports and post-release monitoring. Use when the user
  mentions Google Play, Play Console, publish, release, store listing, AAB, app bundle, rollout,
  internal testing, closed testing, production track, Data safety form, app rejection, target API
  level, ASO, screenshots, or asks how to get an app onto the store.
version: 1.0.0
license: MIT
category: delivery
tags: [android, google-play, release, aso, compliance, rollout, store]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, WebFetch]
metadata:
  maturity: stable
  arabic_summary: "تجهيز ونشر إصدارات أندرويد على Google Play: الامتثال، التوقيع، المسارات، صفحة المتجر، والخصوصية."
---

# Android Play Release

You are the release manager. A rejected or rolled-back release costs more than a delayed one — so
you **verify compliance before you build**, not after.

## When to use
- Preparing a first launch or any production release.
- Fixing a Play policy rejection or a target-API warning.
- Writing store listing copy, screenshots plan, or the Data safety form.

## When NOT to use
- Building the pipeline itself → `android-cicd-github-actions`.
- Icon/graphic asset production → `app-icon-designer`, `logo-brand-designer`.

## Non-negotiables
- **MUST** publish an **Android App Bundle (.aab)**; APKs are not accepted for new apps.
- **MUST** meet the current target API requirement (see pins) before submission — Play Console rejects the upload otherwise.
- **MUST** enrol in **Play App Signing** and protect the upload key; losing it without enrolment is unrecoverable.
- **MUST** make `versionCode` strictly increasing and never reused; `versionName` follows SemVer.
- **MUST** complete Data safety, content rating, ads declaration, target audience, government-app and financial-features forms **truthfully** — mismatches are the top rejection cause.
- **MUST** roll out to production in stages (1% → 5% → 20% → 50% → 100%), watching crash-free rate and ANR between steps.
- **MUST** ship an in-app **account deletion** path plus a public web URL if the app has accounts.
- **NEVER** ship a release that was not first installed and smoke-tested from the **internal testing track** (the exact artifact, signed by Play).
- **NEVER** request `QUERY_ALL_PACKAGES`, `MANAGE_EXTERNAL_STORAGE`, `SMS`/`CALL_LOG`, or accessibility APIs without an approved declaration.
- **NEVER** use screenshots that are not from the actual app, or claims you cannot substantiate.

## Version pins / current requirements
| Requirement | Value |
|---|---|
| Target API for new apps & updates | **API 36 (Android 16)** — required since 2026-08-31 |
| Availability floor for un-updated apps | API 35, or the app disappears for new users |
| Wear OS / Automotive target | API 35 |
| Android TV / XR target | API 34 |
| Developer verification | required from 2026-09-30 (phased by country) |
| New personal accounts | 20 testers × 14 continuous days of closed testing before production |
| Upload format | AAB, ≤ 200 MB base (use Play Asset/Feature Delivery beyond) |
| Signing | Play App Signing mandatory |

> Always re-verify at https://support.google.com/googleplay/android-developer/answer/11926878 before a release.

## Workflow
1. **Pre-flight compliance check** — run the checklist in `references/play-compliance.md`. Stop if anything fails.
2. **Freeze the version**: bump `versionName` (SemVer), set `versionCode` from the CI run number, tag `vX.Y.Z`.
3. **Build the signed AAB** via the release workflow; archive the mapping file.
4. **Internal testing track** — upload, install on ≥ 3 real devices (low-end, mid, tablet/foldable), run the smoke script.
5. **Read the pre-launch report** (Play Console runs your app on real devices): fix crashes, ANRs, accessibility and security findings.
6. **Closed → open testing** if the change is risky or the account is new (20 testers / 14 days rule).
7. **Store listing**: title (30), short description (80), full description (4000), screenshots, feature graphic, what's new (500). See `references/store-listing-aso.md`.
8. **Staged production rollout** with halt criteria defined **in advance**.
9. **Monitor**: crash-free rate, ANR rate, vitals, ratings, and Play policy notifications for 72 hours.
10. **Post-release**: tag the release notes, archive artifacts + mapping, write the retro if anything went wrong.

## Patterns

✅ **Halt criteria defined before rollout**
```
Halt and roll back if, at any stage:
- crash-free sessions < 99.0% (baseline 99.6%)
- ANR rate > 0.47%
- 1-star review rate doubles vs. the previous 7 days
- any P0 functional regression is reported
```

✅ **Version scheme**
```kotlin
versionName = "2.4.1"                       // SemVer, user-visible
versionCode = System.getenv("GITHUB_RUN_NUMBER")?.toInt() ?: 1   // monotonic, never reused
```

✅ **What's new (500 chars, per locale)**
```
• Offline mode: read saved articles with no connection
• 30% faster startup
• Fixed a crash when opening notifications on Android 16
```
Concrete user benefits, not "bug fixes and improvements".

❌ **Don't**
```
- Uploading directly to production "because it's a small fix"
- Data safety says "no data collected" while an analytics SDK sends the advertising ID
- Screenshots with device frames, marketing text overlays that hide the UI, or fake content
- Reusing versionCode 42 after a rollback
```

## Anti-patterns
- Discovering the target-API requirement on release day.
- No internal-track validation — the Play-signed artifact differs from your local build.
- 100% rollout on day one for a release touching payments or auth.
- Ignoring the pre-launch report because "it's just a warning".
- Store listing keyword-stuffed to the point of policy violation.
- Permissions declared "for a future feature".
- Forgetting to update the Data safety form when adding an SDK.
- No changelog discipline → users and reviewers cannot tell what changed.

## Definition of Done
- [ ] `targetSdk` meets the current Play requirement; upload accepted.
- [ ] AAB signed via Play App Signing; upload key backed up offline.
- [ ] Mapping and native symbols uploaded; deobfuscated stack traces confirmed.
- [ ] Internal track install smoke-tested on ≥ 3 devices including a low-end one.
- [ ] Pre-launch report clean of crashes and critical accessibility/security findings.
- [ ] All declarations complete and matching the code (Data safety, ads, content rating, permissions).
- [ ] Account deletion available in-app and via a public URL (if accounts exist).
- [ ] Store listing complete for every supported locale, including Arabic if targeted.
- [ ] Staged rollout plan with written halt criteria.
- [ ] 72-hour monitoring completed; release notes archived.

## References
- `references/play-compliance.md` — the full pre-submission compliance checklist and rejection reasons.
- `references/store-listing-aso.md` — listing copy formulas, asset specs, ASO and localization.
- `references/release-runbook.md` — step-by-step release day runbook, rollback and hotfix procedures.
- Target API requirements: https://support.google.com/googleplay/android-developer/answer/11926878
- Play policy centre: https://play.google.com/about/developer-content-policy/

## ملخص عربي
النشر عملية امتثال قبل أن يكون رفع ملف. تحقّق أولًا من `targetSdk` المطلوب (API 36 حاليًا)،
واستخدم حزمة AAB وتوقيع Play، وارفع أولًا لمسار الاختبار الداخلي وجرّب على أجهزة حقيقية، واقرأ
تقرير ما قبل الإطلاق. املأ نماذج أمان البيانات والتصنيف والإعلانات بصدق تام لأن التناقض هو السبب
الأول للرفض. ثم أطلق تدريجيًا (١٪ ← ١٠٠٪) مع معايير إيقاف مكتوبة مسبقًا ومراقبة ٧٢ ساعة.

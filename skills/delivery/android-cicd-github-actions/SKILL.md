---
name: android-cicd-github-actions
description: >-
  Builds GitHub Actions pipelines for Android: PR validation (lint, detekt, unit tests, screenshot
  tests), instrumented tests on emulators, Gradle caching, signed release AAB/APK builds, artifact
  and mapping upload, GitHub Releases, and Play publishing jobs. Use when the user mentions CI, CD,
  GitHub Actions, workflow, pipeline, automated build, gradle cache, emulator tests, signing in CI,
  release automation, or asks to build the app automatically when code is pushed to a branch.
version: 1.0.0
license: MIT
category: delivery
tags: [android, ci, cd, github-actions, gradle, automation, release]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "خطوط CI/CD لأندرويد عبر GitHub Actions: فحص الطلبات، اختبارات المحاكي، بناء موقّع، ونشر آلي."
---

# Android CI/CD with GitHub Actions

You are the release engineer. The pipeline is the **only** authority on whether the code works.

## When to use
- Creating or fixing GitHub Actions workflows for an Android repo.
- Adding emulator tests, caching, signing, or automated publishing.

## When NOT to use
- Store listing/rollout policy → `android-play-release`.
- Test content itself → `android-testing-quality`.

## Non-negotiables
- **MUST** run on `pull_request` (fast gate) and `push` to the default branch (full gate). Tag pushes trigger release.
- **MUST** use `gradle/actions/setup-gradle` for dependency + build caching, and `actions/setup-java` with the **temurin** JDK 17 distribution.
- **MUST** pin action versions (`@v4`, or a commit SHA for third-party actions). **NEVER** use `@master`.
- **MUST** declare least-privilege `permissions:` at workflow level (`contents: read` by default).
- **MUST** keep all secrets in GitHub Secrets/Environments; decode the keystore to `$RUNNER_TEMP` and delete it in an `if: always()` step.
- **MUST** use `concurrency` with `cancel-in-progress` on PR workflows to avoid queue pile-ups.
- **MUST** upload test reports, lint SARIF and the R8 mapping file as artifacts on every run — including failures.
- **NEVER** run `pull_request_target` with a checkout of untrusted code.
- **NEVER** let a workflow print a secret (`set +x`, no `echo $SECRET`).
- **NEVER** publish to a public track directly from CI without a manual approval environment.

## Version pins
| Item | Value |
|---|---|
| JDK | 17 (temurin) |
| `actions/checkout` | v4 |
| `actions/setup-java` | v4 |
| `gradle/actions/setup-gradle` | v4 |
| `actions/upload-artifact` | v4 |
| `reactivecircus/android-emulator-runner` | v2 |
| `r0adkll/upload-google-play` | v1 |
| Runner | `ubuntu-latest` (macOS only if you need hardware acceleration nuances) |

## Workflow (how to build the pipeline)
1. **Stage 1 — PR gate (< 10 min)**: assemble debug, unit tests, lint, detekt, ktlint, screenshot verification. Fail fast.
2. **Stage 2 — instrumented tests**: emulator matrix (API 28 + 34 + 36) with AVD snapshot caching, run nightly or on the main branch to keep PRs fast.
3. **Stage 3 — release**: on tag `v*`, build the signed AAB + APK, generate a changelog, create a GitHub Release, upload artifacts + mapping.
4. **Stage 4 — publish**: a separate job in a protected `production` Environment requiring manual approval, uploading to the Play internal track.
5. **Cross-cutting**: dependency review, secret scanning (gitleaks), CodeQL, Dependabot/Renovate for `libs.versions.toml`.
6. **Verify**: push a branch and confirm the pipeline runs green end-to-end **before** declaring done.

## Patterns

✅ **PR gate skeleton**
```yaml
name: PR Check
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - uses: gradle/actions/setup-gradle@v4
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
      - run: chmod +x ./gradlew
      - name: Static analysis
        run: ./gradlew --no-daemon detekt lintDebug
      - name: Unit tests
        run: ./gradlew --no-daemon testDebugUnitTest
      - name: Assemble
        run: ./gradlew --no-daemon assembleDebug
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: reports
          path: |
            **/build/reports/**
            **/build/test-results/**
```

✅ **Emulator job with AVD caching**
```yaml
  instrumented:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        api-level: [28, 34, 36]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - uses: gradle/actions/setup-gradle@v4
      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' \
            | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules && sudo udevadm trigger --name-match=kvm
      - uses: actions/cache@v4
        id: avd-cache
        with:
          path: |
            ~/.android/avd/*
            ~/.android/adb*
          key: avd-${{ matrix.api-level }}
      - if: steps.avd-cache.outputs.cache-hit != 'true'
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: ${{ matrix.api-level }}
          arch: x86_64
          force-avd-creation: false
          emulator-options: -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: false
          script: echo "Generated AVD snapshot"
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: ${{ matrix.api-level }}
          arch: x86_64
          force-avd-creation: false
          emulator-options: -no-snapshot-save -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim
          disable-animations: true
          script: ./gradlew connectedDebugAndroidTest
```

❌ **Don't**
```yaml
- run: echo "${{ secrets.KEYSTORE_PASSWORD }}"   # printed to logs forever
- uses: some-user/random-action@master           # unpinned, supply-chain risk
- run: ./gradlew build                           # no cache, no timeout, 40-minute job
```

## Anti-patterns
- One monolithic job doing lint + tests + emulator + release (slow feedback, no parallelism).
- Caching `~/.gradle` manually instead of `setup-gradle` (corrupt caches, no cache key hygiene).
- Running instrumented tests on every PR when they take 25 minutes — move them to main/nightly.
- Committing the keystore "encrypted with a password in the repo".
- `continue-on-error: true` on the test step to keep the build green.
- Releasing from a branch instead of an immutable tag.
- No `timeout-minutes` → a hung emulator burns six hours of runner time.

## Definition of Done
- [ ] PR gate finishes in < 10 minutes and blocks merge on failure (branch protection enabled).
- [ ] Cache hit rate visible and > 70% on unchanged dependencies.
- [ ] Instrumented tests run on at least 3 API levels with AVD snapshot caching.
- [ ] Release workflow produces a signed AAB + APK + mapping.txt attached to a GitHub Release.
- [ ] Play publish job sits behind a protected Environment with manual approval.
- [ ] No secret is ever echoed; keystore file shredded after use.
- [ ] All actions pinned; `permissions` least-privilege.
- [ ] A real run of each workflow is green and linked in the PR.

## References
- `references/workflow-recipes.md` — complete copy-paste workflows (PR, release, publish, nightly).
- `references/ci-hardening.md` — permissions, OIDC, supply-chain, cost and speed tuning.
- `templates/github-workflows/` in this repo — ready-to-copy working examples.
- GitHub Actions docs: https://docs.github.com/actions

## ملخص عربي
خط الإنتاج هو الحكم الوحيد على صحة الكود. ابنِ بوابة سريعة لطلبات الدمج (فحص ساكن + اختبارات
وحدات + بناء) أقل من ١٠ دقائق، واختبارات المحاكي على مصفوفة إصدارات في مسار منفصل، وبناء إصدار
موقّع عند وسم `v*` مع رفع AAB وملف mapping، ثم وظيفة نشر محمية بموافقة يدوية. ثبّت إصدارات
الـ actions، وامنح أقل الصلاحيات، ولا تطبع أي سر، واحذف ملف التوقيع بعد الاستخدام دائمًا.

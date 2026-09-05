---
name: android-project-bootstrap
description: >-
  Scaffolds a modern, production-grade Android project with Gradle Kotlin DSL, a TOML version
  catalog, convention plugins, multi-module structure, JDK 17 toolchain and quality gates
  (detekt, ktlint, lint). Use when the user asks to create, bootstrap, scaffold, migrate or
  restructure an Android app or library project, mentions build.gradle.kts, settings.gradle.kts,
  libs.versions.toml, AGP, Gradle wrapper, buildSrc, build-logic, product flavors, or says
  "new Android app", "Kotlin project setup", or "clean up my Gradle files".
version: 1.0.0
license: MIT
category: android
tags: [android, gradle, kotlin, agp, version-catalog, scaffolding]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, WebFetch]
metadata:
  maturity: stable
  arabic_summary: "إنشاء مشروع أندرويد حديث ببنية موديولات، كتالوج إصدارات، وإضافات اتفاقية وبوابات جودة."
---

# Android Project Bootstrap

You are a build engineer. You create Android projects that a team of 20 can scale for five years —
not a single-module demo.

## When to use
- Creating a new Android app or library from zero.
- Restructuring a legacy single-module project into modules.
- Standardising build files: version catalog, convention plugins, toolchains.

## When NOT to use
- Writing UI code → `android-compose-ui`.
- Layer/dependency design decisions → `android-kotlin-architecture`.
- CI pipelines → `android-cicd-github-actions`.

## Non-negotiables
- **MUST** use Gradle **Kotlin DSL** (`.kts`) and a **version catalog** (`gradle/libs.versions.toml`). No hardcoded versions in module build files.
- **MUST** put shared build logic in `build-logic/` convention plugins. **NEVER** copy-paste `android { }` blocks across modules.
- **MUST** set `compileSdk` = latest stable, `targetSdk` = Play requirement (see pins), `minSdk` ≥ 24 unless the user justifies lower.
- **MUST** commit the Gradle wrapper (`gradlew`, `gradle-wrapper.jar/properties`) and pin `distributionSha256Sum`.
- **MUST** enable `org.gradle.caching=true`, `org.gradle.configuration-cache=true`, `org.gradle.parallel=true`.
- **MUST** apply a JDK **17** toolchain explicitly — never rely on the machine's JDK.
- **NEVER** commit `local.properties`, `*.jks`, `*.keystore`, `google-services.json` with real keys, or `/build`.
- **NEVER** use dynamic versions (`1.2.+`, `latest.release`) or `allprojects { repositories { } }` (use `dependencyResolutionManagement`).

## Version pins
| Component | Version | Note |
|---|---|---|
| AGP | 9.1.x | Kotlin support is **built in**; do not apply `org.jetbrains.kotlin.android` for app/library modules |
| Gradle | 9.3.x | AGP 9.1 minimum |
| Kotlin | 2.3.x | Compose compiler plugin version == Kotlin version |
| JDK | 17 | AGP 9 minimum & default |
| compileSdk | 36 | Android 16 |
| targetSdk | 36 | Required by Google Play for new apps & updates since 2026-08-31 |
| minSdk | 24 | ~99% device reach |
| Compose BOM | 2026.08.00 | Single source for all Compose versions |
| NDK (if used) | 28.2.13676358 | AGP 9 default |

> Before pinning, verify against the release notes; if a newer stable exists, use it and update this table.

## Workflow
1. **Interrogate**: app name, package id (`com.company.app`), minSdk, UI toolkit (Compose default), offline needs, target form factors.
2. **Create the skeleton** (see `references/project-skeleton.md` for the full tree):
   `app/`, `core/{ui,designsystem,data,domain,common,testing}/`, `feature/<name>/`, `build-logic/`.
3. **Write `gradle/libs.versions.toml`** — every dependency and plugin declared once, grouped in bundles.
4. **Write convention plugins** in `build-logic/convention/` (`android.application`, `android.library`, `android.compose`, `android.hilt`, `jvm.library`, `android.test`).
5. **Configure `gradle.properties`** (caching, config cache, `android.useAndroidX=true`, `-Xmx4g`).
6. **Add quality gates**: detekt + ktlint + Android Lint with `abortOnError = true`; a `spotless`/`.editorconfig` for formatting.
7. **Add `.gitignore`, `README.md`, `LICENSE`, `CODEOWNERS`, `renovate.json`.**
8. **Verify**: `./gradlew --no-daemon clean assembleDebug lint detekt test` must pass before you report success.
9. Hand off to `android-cicd-github-actions` to make CI enforce step 8.

## Patterns

✅ **Module `build.gradle.kts` after convention plugins**
```kotlin
plugins {
    alias(libs.plugins.myapp.android.library)
    alias(libs.plugins.myapp.android.hilt)
}

android { namespace = "com.company.app.core.data" }

dependencies {
    api(projects.core.domain)
    implementation(libs.bundles.network)
    testImplementation(libs.bundles.testing)
}
```

❌ **Don't**
```kotlin
android {
    compileSdk = 36                 // duplicated in 14 modules
    defaultConfig { minSdk = 24 }
}
dependencies {
    implementation("com.squareup.retrofit2:retrofit:2.11.0") // hardcoded, drifts
}
```

✅ **`gradle/libs.versions.toml` shape**
```toml
[versions]
agp = "9.1.1"
kotlin = "2.3.21"
composeBom = "2026.08.00"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }

[bundles]
compose = ["androidx-compose-material3", "androidx-compose-ui", "androidx-compose-ui-tooling-preview"]

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
myapp-android-library = { id = "myapp.android.library" }
```

## Anti-patterns
- `buildSrc` for build logic (invalidates the whole build cache on change) → use `build-logic` as an included build.
- One giant `:app` module — impossible to parallelise or test in isolation.
- `implementation` everywhere including public API types → leaks compile errors; use `api` deliberately.
- Committing `keystore.properties` "just for now".
- Product flavors used to model *layers* instead of *distribution variants*.

## Definition of Done
- [ ] `./gradlew clean assembleDebug` succeeds from a clean clone.
- [ ] Zero hardcoded dependency versions outside `libs.versions.toml`.
- [ ] No `android { }` config duplicated across modules.
- [ ] `lint`, `detekt`, `ktlint`, `test` all wired and green.
- [ ] Wrapper committed with SHA-256 pinned; JDK 17 toolchain declared.
- [ ] `.gitignore` blocks build outputs, keystores, `local.properties`.
- [ ] Second clean build is > 60% faster (build cache works).
- [ ] README documents commands: build, test, lint, release.

## References
- `references/project-skeleton.md` — full directory tree + starter file contents.
- `references/gradle-performance.md` — caching, config cache, module graph rules.
- Android Gradle plugin release notes: https://developer.android.com/build/releases/gradle-plugin
- Now in Android (reference multi-module project): https://github.com/android/nowinandroid

## ملخص عربي
هذه المهارة تُنشئ هيكل مشروع أندرويد احترافي: Kotlin DSL، كتالوج إصدارات TOML واحد، إضافات
اتفاقية في `build-logic` بدل التكرار، تقسيم إلى موديولات (`app` / `core` / `feature`)، تفعيل
الكاش وذاكرة التهيئة، وبوابات جودة (detekt، ktlint، lint). ممنوع تثبيت الإصدارات داخل ملفات
الموديولات أو رفع مفاتيح التوقيع. لا يُعلن الإنجاز إلا بعد نجاح `assembleDebug` و`lint` و`test`.

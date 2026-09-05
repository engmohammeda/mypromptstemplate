# Static analysis & quality gates — reference

## 1. The gate set

| Tool | Catches | Fails build on |
|---|---|---|
| Android Lint | API misuse, resource issues, a11y, security, performance | any `error`-severity issue |
| detekt | complexity, code smells, potential bugs, formatting (with `detekt-formatting`) | `maxIssues: 0` |
| ktlint / spotless | style, import order, formatting | any violation |
| Kover | coverage regression | below threshold |
| dependency-analysis | unused/misdeclared dependencies | `buildHealth` failures |
| Roborazzi/Paparazzi | unintended visual change | golden mismatch |

Aggregate them: `./gradlew check` must run all of the above.

## 2. Android Lint configuration

```kotlin
android {
    lint {
        abortOnError = true
        warningsAsErrors = true
        checkDependencies = true
        checkReleaseBuilds = true
        baseline = file("lint-baseline.xml")   // only for legacy adoption; shrink it every sprint
        disable += setOf("GradleDependency")   // justify every disable in a comment
        sarifOutput = file("build/reports/lint.sarif")  // upload to GitHub code scanning
    }
}
```

High-value checks to never disable: `Recycle`, `HandlerLeak`, `StaticFieldLeak`,
`UnsafeIntentLaunch`, `ExportedActivity`, `HardcodedText`, `ContentDescription`,
`SetJavaScriptEnabled`, `TrustAllX509TrustManager`, `MissingPermission`.

## 3. detekt

```kotlin
detekt {
    buildUponDefaultConfig = true
    allRules = false
    config.setFrom(files("$rootDir/config/detekt/detekt.yml"))
    parallel = true
}
tasks.withType<Detekt>().configureEach {
    reports { sarif.required.set(true); html.required.set(true) }
    jvmTarget = "17"
}
dependencies { detektPlugins(libs.detekt.formatting) }
```

Key thresholds in `detekt.yml`:
```yaml
build:
  maxIssues: 0
complexity:
  LongMethod: { threshold: 40 }
  LongParameterList: { functionThreshold: 6, constructorThreshold: 7 }
  CyclomaticComplexMethod: { threshold: 12 }
  TooManyFunctions: { thresholdInClasses: 15 }
exceptions:
  TooGenericExceptionCaught: { active: true }
  SwallowedException: { active: true }
potential-bugs:
  UnsafeCallOnNullableType: { active: true }
  LateinitUsage: { active: true }
naming:
  FunctionNaming: { ignoreAnnotated: ['Composable'] }   # Composables are PascalCase
```

## 4. Compose-specific lint
Add the **Compose rules** for detekt or `slack/compose-lints`:
- `ComposableParamOrder` — `Modifier` first optional param.
- `ModifierMissing` / `ModifierNotUsedAtRoot`.
- `ComposableNaming` — PascalCase for UI, camelCase for value-returning.
- `UnstableCollections` — flags `List<T>` params.
- `ViewModelForwarding` — bans passing a ViewModel to child composables.
- `Material2` — bans accidental M2 imports in an M3 app.

## 5. Kover

```kotlin
kover {
    reports {
        filters {
            excludes {
                classes(
                    "*_Factory", "*_HiltModules*", "*Hilt_*", "*_Impl",
                    "*.BuildConfig", "*ComposableSingletons*", "*Preview*",
                )
            }
        }
        verify {
            rule("line coverage") {
                bound { minValue = 60; coverageUnits = CoverageUnit.LINE }
            }
            rule("branch coverage on domain") {
                bound { minValue = 80; coverageUnits = CoverageUnit.BRANCH }
            }
        }
    }
}
```

## 6. Pre-commit hook (fast subset)

`.git/hooks/pre-commit` (install via a Gradle task so the whole team gets it):
```bash
#!/bin/sh
./gradlew --quiet ktlintCheck detektMain || {
  echo "❌ style/static analysis failed — run ./gradlew ktlintFormat"; exit 1;
}
```
Keep the hook under 20 seconds; the full suite belongs in CI.

## 7. Reporting to GitHub
Upload SARIF from lint and detekt so issues appear inline on the PR:
```yaml
- uses: github/codeql-action/upload-sarif@v3
  with: { sarif_file: app/build/reports/lint.sarif }
```

## 8. Ratchet policy
- New code: zero warnings, no baseline entries.
- Legacy: baseline allowed, but every PR touching a file must remove its baseline entries.
- The baseline file size must monotonically decrease — enforce with a CI check.

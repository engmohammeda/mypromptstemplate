# Gradle performance & module graph — reference

## Budgets
| Metric | Target |
|---|---|
| Clean `assembleDebug` (CI, cold cache) | < 6 min |
| Incremental build after one-line UI change | < 30 s |
| Configuration time | < 3 s (with configuration cache) |
| Cache hit rate on CI for unchanged modules | > 80% |

## The seven levers

1. **Configuration cache** — `org.gradle.configuration-cache=true`. Fix violations rather than disabling it
   (no `Project` access at execution time, no `System.getenv` in task actions — use `providers.environmentVariable`).
2. **Build cache** — local + remote (`buildCache { remote<HttpBuildCache> { ... } }` in `settings.gradle.kts`).
3. **Module granularity** — many small modules parallelise; but > 150 modules costs configuration time.
   Rule of thumb: a module should be buildable in < 20 s.
4. **`api` vs `implementation`** — every `api` widens the recompilation blast radius. Default to `implementation`.
5. **KSP over KAPT** — KAPT forces Java stub generation. Migrate Room/Hilt/Moshi to KSP.
6. **Disable unused build features** — `buildConfig`, `resValues`, `aidl`, `renderScript`, `shaders` off by default.
7. **Non-transitive R classes** — `android.nonTransitiveRClass=true` shrinks R classes dramatically.

## Diagnosis commands

```bash
./gradlew assembleDebug --scan                     # build scan: where time goes
./gradlew assembleDebug --profile                  # HTML report in build/reports/profile
./gradlew :app:dependencies --configuration releaseRuntimeClasspath
./gradlew buildHealth                              # with the dependency-analysis plugin
./gradlew projectHealth                            # unused/misused dependencies per module
```

Add the **dependency analysis** plugin to catch wrong `api`/`implementation` and unused deps:
```kotlin
plugins { id("com.autonomousapps.dependency-analysis") version "<latest>" }
```

## Dependency hygiene
- Renovate/Dependabot on `gradle/libs.versions.toml`, grouped PRs, weekly.
- `./gradlew dependencyUpdates` (Ben Manes plugin) before each release.
- Verify checksums for critical dependencies with Gradle dependency verification
  (`gradle/verification-metadata.xml`) on release builds.

## Common configuration-cache violations and fixes

| Violation | Fix |
|---|---|
| `System.getenv("X")` in a task | `providers.environmentVariable("X")` |
| `project.version` read at execution | capture into a `@Input` property at configuration time |
| `File` from `project.file()` in `doLast` | inject via `@InputFile RegularFileProperty` |
| Custom plugin holding `Project` reference | hold only serialisable providers |

---
name: android-performance
description: >-
  Measures and fixes Android performance: cold/warm startup time, jank and frame timing, Baseline
  and Startup Profiles, memory leaks, battery and background work, R8 shrinking, and APK/AAB size.
  Use when the user mentions slow app, startup time, jank, dropped frames, ANR, OOM, memory leak,
  battery drain, app size, APK size, R8, ProGuard, macrobenchmark, baseline profile, or asks to
  optimize or profile an Android app.
version: 1.0.0
license: MIT
category: android
tags: [android, performance, startup, jank, baseline-profile, r8, app-size, memory]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "قياس وتحسين أداء تطبيقات أندرويد: زمن الإقلاع، الإطارات، الذاكرة، البطارية، وحجم الحزمة."
---

# Android Performance

You are a performance engineer. You **measure first, fix second, and prove the fix with numbers**.

## When to use
- The app feels slow, janky, heavy, or is flagged by Play Console vitals.
- Before a release: guarding startup/frame/size budgets.

## When NOT to use
- Correctness bugs → `android-testing-quality`.
- Compose-specific recomposition detail → `android-compose-ui` (see its `compose-performance` reference).

## Non-negotiables
- **MUST** benchmark on a **release-like build** (`minifyEnabled`, non-debuggable) on a **real mid-range device**. Emulator and debug numbers are meaningless.
- **MUST** state a baseline number before optimizing and the delta after. **NEVER** claim an improvement without a measurement.
- **MUST** ship a **Baseline Profile** for any app with Compose or a startup > 300 ms.
- **MUST** keep `isMinifyEnabled = true` and `isShrinkResources = true` for release, with R8 full mode.
- **MUST** upload the R8 mapping file for every release build.
- **NEVER** do disk or network I/O on the main thread; **NEVER** initialize SDKs eagerly in `Application.onCreate` without measuring their cost.
- **NEVER** optimize by guessing (`I think this loop is slow`) — profile with Perfetto/Android Studio Profiler.

## Budgets (defaults; tighten per product)
| Metric | Target |
|---|---|
| Cold start (TTID, mid-range) | < 500 ms (Play warns > 5 s) |
| Cold start (TTFD) | < 1000 ms |
| Frame time P99 | < 16 ms (60Hz) / < 8 ms (120Hz) |
| Frozen frames | 0 in critical flows (> 700 ms) |
| ANR rate | < 0.47% (Play bad-behaviour threshold) |
| Crash-free sessions | > 99.5% |
| Download size (AAB) | < 20 MB, warn at 30 MB |
| Memory (mid-range, steady) | < 200 MB PSS |
| `Application.onCreate` | < 100 ms |

## Workflow
1. **Reproduce & measure**: `Macrobenchmark` for startup + scroll; `adb shell am start-activity -W`; Perfetto trace for anything > 16 ms.
2. **Read Play Console Android vitals** (ANRs, excessive wakeups, stuck partial wake locks, slow frames) — real-user data beats local runs.
3. **Fix startup**: lazy-init SDKs with `androidx.startup` Initializer, remove `ContentProvider` auto-inits, defer non-critical work to after first frame, avoid heavy DI graph creation, keep the splash to `SplashScreen` API.
4. **Fix jank**: find the long frame in Perfetto → main-thread work, layout thrash, unbounded lists, synchronous image decode.
5. **Generate Baseline + Startup Profiles** with the `androidx.baselineprofile` plugin; regenerate whenever the startup path changes.
6. **Fix memory**: LeakCanary in debug, heap dump for retained objects, bitmaps downsampled to the view size, caches bounded (`LruCache`).
7. **Fix battery**: WorkManager with constraints, no polling, batch network, respect Doze/App Standby buckets.
8. **Shrink size**: `AAB` + `enableSplit`, R8 full mode, remove unused resources/assets, WebP/AVIF images, vector drawables, analyse with APK Analyzer.
9. **Guard in CI**: benchmark job on a real device or Firebase Test Lab + size check on every PR.

## Patterns

✅ **Macrobenchmark: startup**
```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule val rule = MacrobenchmarkRule()

    @Test fun coldStartupWithBaselineProfile() = rule.measureRepeated(
        packageName = "com.company.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.Partial(BaselineProfileMode.Require),
    ) {
        pressHome()
        startActivityAndWait()
    }
}
```

✅ **Baseline profile generation**
```kotlin
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule val rule = BaselineProfileRule()

    @Test fun generate() = rule.collect(packageName = "com.company.app") {
        pressHome(); startActivityAndWait()
        device.findObject(By.res("home_list")).fling(Direction.DOWN)
        device.waitForIdle()
    }
}
```
Run: `./gradlew :app:generateReleaseBaselineProfile` → commit `app/src/release/generated/baselineProfiles/`.

✅ **Deferred initialization**
```kotlin
class AnalyticsInitializer : Initializer<Analytics> {
    override fun create(context: Context): Analytics = Analytics.init(context)
    override fun dependencies() = emptyList<Class<out Initializer<*>>>()
}
```
Better: initialise after the first frame via `Choreographer.postFrameCallback` or a `WorkManager` task.

❌ **Don't**
```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        Firebase.initialize(this)      // 120 ms
        Fresco.initialize(this)        // 90 ms
        val db = Room.databaseBuilder(...).build().openHelper.writableDatabase // disk I/O!
        loadUserPreferencesBlocking()  // main-thread SharedPreferences read
    }
}
```

## Anti-patterns
- Micro-optimizing Kotlin collections while a 400 ms main-thread JSON parse sits untouched.
- `SharedPreferences.getX()` on the main thread at startup (use DataStore, read async).
- Full-size bitmaps loaded into thumbnails (use Coil with `size()`).
- Unbounded in-memory caches → OOM on low-RAM devices.
- `setJavaScriptEnabled` WebViews created eagerly on startup.
- Disabling R8 to "fix" a crash instead of adding the correct `-keep` rule.
- Shipping debug logging and `StrictMode` violations to production.
- `AlarmManager` exact alarms for background sync (use WorkManager).

## Definition of Done
- [ ] Startup, frame and size numbers recorded **before and after**, on the same device.
- [ ] Baseline Profile generated, committed, and verified to improve startup (usually 15–30%).
- [ ] Macrobenchmark for startup + primary scroll is in CI with thresholds.
- [ ] Zero main-thread I/O (StrictMode clean in debug).
- [ ] LeakCanary: no leaks in the top 5 flows.
- [ ] R8 full mode on, mapping uploaded, no over-broad `-keep class **`.
- [ ] AAB download size within budget; APK Analyzer diff reviewed.
- [ ] Play Console vitals: ANR and crash rates under thresholds after rollout.

## References
- `references/startup-and-jank.md` — measurement commands, Perfetto reading, startup checklist.
- `references/app-size-and-r8.md` — shrinking, keep rules, resource/asset optimization, size CI gate.
- App startup docs: https://developer.android.com/topic/performance/vitals/launch-time

## ملخص عربي
لا تحسين بلا قياس: نفّذ القياس على بناء إصدار حقيقي وجهاز متوسط، وسجّل الرقم قبل وبعد. ركّز على
زمن الإقلاع (تأجيل تهيئة المكتبات، Baseline Profile)، وسلاسة الإطارات (تتبّع Perfetto)، والذاكرة
(LeakCanary وحدود للكاش)، والبطارية (WorkManager بقيود)، وحجم الحزمة (AAB + R8 + صور مضغوطة).
احرس كل ذلك بميزانيات أرقام في الـ CI.

# Startup & jank — reference

## 1. Measure

```bash
# Cold start, 10 runs
adb shell am force-stop com.company.app
adb shell am start-activity -W -n com.company.app/.MainActivity   # read TotalTime

# Frame stats for the last window
adb shell dumpsys gfxinfo com.company.app framestats

# System trace (open in ui.perfetto.dev)
adb shell perfetto -o /data/misc/perfetto-traces/trace -t 20s sched freq idle am wm gfx view binder_driver hal dalvik
adb pull /data/misc/perfetto-traces/trace

# Startup breakdown from logcat
adb logcat -d | grep "Displayed"
```

Definitions: **TTID** = time to initial display (first frame drawn). **TTFD** = time to full display
— call `reportFullyDrawn()` (or `ReportDrawn` in Compose) when real content is on screen, otherwise
Play measures the wrong thing.

## 2. Startup cost checklist (in order of usual impact)

| Cost | Typical | Fix |
|---|---|---|
| Third-party SDK init in `Application.onCreate` | 50–400 ms | `androidx.startup`, lazy init, init after first frame |
| Auto-initializing `ContentProvider`s | 20–150 ms | remove via manifest merger `tools:node="remove"` |
| Dependency graph construction | 20–100 ms | `Lazy<T>`/`Provider<T>`, avoid eager singletons |
| Main-thread SharedPreferences | 10–80 ms | DataStore, read async, cache in memory |
| Database open + migration | 30–200 ms | open lazily off the main thread |
| Layout inflation / first composition | 50–200 ms | Baseline Profile, simpler first screen |
| Splash animation held artificially | any | `SplashScreen` API with `setKeepOnScreenCondition` bounded |
| No AOT profile (JIT interpreting) | 20–40% of total | Baseline + Startup Profile |

Manifest removal of a provider:
```xml
<provider
    android:name="com.thirdparty.SdkInitProvider"
    android:authorities="${applicationId}.sdk-init"
    tools:node="remove" />
```

## 3. StrictMode in debug (catch main-thread I/O at development time)

```kotlin
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder().detectAll().penaltyLog().penaltyDeath().build()
    )
    StrictMode.setVmPolicy(
        StrictMode.VmPolicy.Builder().detectAll().penaltyLog().build()
    )
}
```

## 4. Reading a Perfetto trace for jank
1. Filter to your app's main thread track.
2. Find frames marked **Janky** in the *Expected/Actual Timeline* tracks.
3. Zoom into the actual frame slice; the widest child slice is your culprit.
4. Common culprits and signatures:

| Slice | Meaning | Fix |
|---|---|---|
| `Choreographer#doFrame` long in `traversal` | layout/measure too deep or too many views | flatten hierarchy, `LazyColumn`, avoid nested weights |
| `inflate` during scroll | view inflated per item | recycle, or Compose |
| `Bitmap.decode*` | image decoded on main thread | Coil/Glide off-thread with size |
| `binder transaction` | synchronous IPC (PackageManager, ContentResolver) | cache results, move off main |
| GC slices (`concurrent copying GC`) | allocation churn per frame | reuse objects, avoid allocations in `onDraw`/composition |
| SQLite `query` | DB on main thread | Flow + IO dispatcher |

## 5. Baseline & Startup Profiles

Setup:
```kotlin
// app/build.gradle.kts
plugins { alias(libs.plugins.androidx.baselineprofile) }
dependencies { baselineProfile(projects.benchmark) }
baselineProfile { automaticGenerationDuringBuild = false }
```
- **Baseline Profile** → AOT-compiles hot paths. Typical gain: 15–30% faster startup, fewer janky frames on first runs.
- **Startup Profile** → additionally reorders DEX so startup classes sit together.
- Regenerate on every meaningful UI/startup change; treat a stale profile as a bug.
- Verify it is actually applied: `CompilationMode.Partial(BaselineProfileMode.Require)` in the benchmark fails if missing.

## 6. ANR prevention
- Any main-thread block > 5 s (input) or > 10 s (broadcast) = ANR.
- Frequent causes: synchronous IPC, deadlocks on locks held by IO, `BroadcastReceiver.onReceive` doing work, `Application.onCreate` heavy init, `SharedPreferences.commit()`.
- Use `ApplicationExitInfo` to collect ANR reasons in the field.
- Broadcast receivers: `goAsync()` or hand off to WorkManager immediately.

## 7. Memory
```bash
adb shell dumpsys meminfo com.company.app
```
- Watch **PSS** and **Java heap**. A steadily rising heap across navigation = leak.
- LeakCanary in debug; heap dump → dominator tree → find the retaining path.
- Bitmaps: request the display size, use `Bitmap.Config.RGB_565` when alpha is not needed for large images.
- Bound every cache; prefer `LruCache` sized from `ActivityManager.memoryClass`.
- Beware: `Activity` context captured by a singleton, static `View`, non-static inner `Handler`, un-disposed Rx/Flow collectors.

## 8. Battery & background
- WorkManager with `Constraints` (network, charging, battery-not-low); no polling loops.
- Batch network calls; use push (FCM) instead of periodic sync where possible.
- Foreground services need a declared `foregroundServiceType` and a real user-visible reason.
- Watch Play Console "excessive wakeups" and "stuck partial wake locks" vitals.
- Test in Doze: `adb shell dumpsys deviceidle force-idle`.

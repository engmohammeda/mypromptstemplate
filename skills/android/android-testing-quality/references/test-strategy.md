# Test strategy — reference

## 1. What to test where

| Level | Runs on | Use for | Budget |
|---|---|---|---|
| Unit (JVM) | JVM, no Android | use cases, ViewModels, mappers, validators, formatters | < 50 ms/test |
| Robolectric | JVM with Android shadows | Activity/Fragment logic, resources, `Context` helpers | < 500 ms/test |
| Instrumented integration | emulator/device | Room, DataStore, WorkManager, permissions | < 5 s/test |
| Compose UI | emulator or Robolectric | one happy path per critical flow | < 10 s/test |
| Screenshot | JVM (Paparazzi/Roborazzi) | design system + screen appearance | < 1 s/test |
| Macrobenchmark | real device | startup, scroll, baseline profiles | separate CI job |

## 2. The behaviour checklist for every screen
- [ ] initial load
- [ ] success with data
- [ ] success with empty list
- [ ] network error → error UI + retry works
- [ ] offline → cached content shown
- [ ] slow response → loading indicator, no duplicate requests
- [ ] permission denied (if applicable) → rationale path
- [ ] rotation / process death → state restored
- [ ] rapid double-tap on the primary action → single side effect
- [ ] back navigation from every sub-state

## 3. Fakes catalogue (put in `core:testing`)

```kotlin
class TestClock(var now: Instant = Instant.parse("2026-01-01T00:00:00Z")) : Clock() { ... }

class FakeNetworkMonitor : NetworkMonitor {
    private val state = MutableStateFlow(true)
    override val isOnline: Flow<Boolean> = state
    fun setOnline(value: Boolean) { state.value = value }
}

object TestData {
    fun article(id: String = "1", title: String = "Title") = Article(id, title, ...)
}
```

**Rule:** a fake implements the real interface and holds real (simple) behaviour. A mock returns
canned answers. Fakes survive refactors; mocks do not.

## 4. Coroutine testing rules
- `runTest { }` for anything suspending; it skips `delay` virtually.
- `UnconfinedTestDispatcher` when you want eager execution (most ViewModel tests).
- `StandardTestDispatcher` + `advanceUntilIdle()` when you must control ordering.
- Never `runBlocking` in tests of suspending code.
- `backgroundScope` for collectors that should be cancelled at test end.
- Turbine: `awaitItem()`, `expectMostRecentItem()`, `awaitComplete()`, `cancelAndIgnoreRemainingEvents()`.
- If a test needs `delay(1000)` in real time, your production code has a hidden dispatcher.

## 5. Flakiness playbook

| Symptom | Root cause | Fix |
|---|---|---|
| Passes locally, fails in CI | timing/dispatcher, screen size, locale | inject dispatchers; pin emulator config & locale |
| Fails only when run with others | shared state | reset singletons in `@After`; `@HiltAndroidTest` fresh graph |
| Espresso "root not found" | animations enabled | disable window/transition/animator scales on the emulator |
| Random ordering failures | unordered collections asserted | assert with `containsExactlyInAnyOrder` |
| Network-dependent | real API | MockWebServer with recorded responses |
| Time-dependent | `System.currentTimeMillis()` | inject `Clock` |

CI emulator hardening:
```bash
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
```

## 6. Screenshot testing (Roborazzi — runs on JVM, no emulator)
```kotlin
@RunWith(AndroidJUnit4::class)
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel7)
class ArticleCardScreenshotTest {
    @get:Rule val composeRule = createComposeRule()

    @Test fun articleCard_light() {
        composeRule.setContent { AppTheme(darkTheme = false) { ArticleCard(TestData.article()) } }
        composeRule.onRoot().captureRoboImage()
    }
}
```
Commands: `./gradlew recordRoborazziDebug` to update goldens, `verifyRoborazziDebug` in CI.
Review golden diffs in the PR — a changed pixel must be an intentional design change.

## 7. Hilt in tests
```kotlin
@HiltAndroidTest
@UninstallModules(NetworkModule::class)
class HomeFlowTest {
    @get:Rule(order = 0) val hiltRule = HiltAndroidRule(this)
    @get:Rule(order = 1) val composeRule = createAndroidComposeRule<MainActivity>()

    @BindValue @JvmField val repository: ArticleRepository = FakeArticleRepository()
}
```
Use `HiltTestRunner` as the `testInstrumentationRunner`.

## 8. Coverage policy
- Measure with **Kover** (Kotlin-aware) — `koverVerify` in `check`.
- Exclude: generated code (`*_Impl`, `*Hilt*`, `*Binding`), DI modules, `*Preview*`, data classes with no logic.
- Ratchet: threshold may only increase. A PR that lowers coverage fails.
- Meaningful target: 80% on `domain` and `data`, 60% on `feature`, none demanded on `app`.

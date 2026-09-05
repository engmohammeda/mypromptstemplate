---
name: android-testing-quality
description: >-
  Designs and writes the Android test strategy: unit tests for ViewModels and use cases with
  coroutines and Turbine, Room and repository integration tests, Compose UI tests, screenshot
  tests, and static analysis gates (detekt, ktlint, Android Lint). Use when the user mentions
  tests, testing, JUnit, MockK, Turbine, Robolectric, Espresso, createAndroidComposeRule, coverage,
  flaky tests, test doubles, screenshot testing, Paparazzi, Roborazzi, or asks how to verify
  Android code or set up quality gates.
version: 1.0.0
license: MIT
category: android
tags: [android, testing, junit, compose-test, coverage, static-analysis, quality]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "استراتيجية اختبار أندرويد كاملة: وحدات، تكامل، واجهة، لقطات شاشة، وبوابات تحليل ساكن."
---

# Android Testing & Quality

You are the QA architect. A feature is not done when it compiles — it is done when a **test proves
it** and a **gate protects it**.

## When to use
- Adding tests to new or existing Android code.
- Setting up test infrastructure, fakes, coverage and static-analysis gates.
- Diagnosing flaky or slow tests.

## When NOT to use
- Performance benchmarking → `android-performance`.
- Security testing → `android-security-hardening`.

## Non-negotiables
- **MUST** follow the pyramid: ~70% unit (JVM), ~20% integration, ~10% end-to-end UI. **NEVER** invert it.
- **MUST** test **behaviour**, not implementation. **NEVER** assert on private fields or method-call counts of internals.
- **MUST** use **fakes over mocks** for your own interfaces. Mock only third-party/awkward boundaries.
- **MUST** make tests deterministic: injected `TestDispatcher`, fixed `Clock`, seeded random, no `Thread.sleep`, no real network.
- **MUST** name tests as `methodName_condition_expectedResult` (or backtick sentences in Kotlin).
- **MUST** make CI fail on: any failing test, detekt/ktlint violation, `lint` error, coverage drop below the agreed threshold.
- **NEVER** commit `@Ignore`d tests without a linked issue and a date.
- **NEVER** use `Thread.sleep` or `IdlingPolicies` timeouts to "fix" flakiness — fix the synchronisation.
- **NEVER** let a test depend on execution order or on another test's state.

## Version pins
| Component | Version |
|---|---|
| JUnit | 4.13.2 (Android instrumented) / JUnit 5 for JVM modules |
| kotlinx-coroutines-test | 1.10.x |
| Turbine | 1.2.x |
| MockK | 1.14.x |
| Truth / assertk | latest stable |
| Robolectric | 4.15.x |
| androidx.test.ext:junit | 1.3.x |
| Roborazzi / Paparazzi | latest stable |

## Workflow
1. **Define the test plan** with the feature: list behaviours (happy, empty, error, offline, permission denied, slow network, rotation).
2. **Write the ViewModel test first** — it is the cheapest place to encode the spec.
3. **Build fakes** in `core:testing` (`FakeArticleRepository`, `TestClock`, `MainDispatcherRule`).
4. **Add Room/repository integration tests** with an in-memory database.
5. **Add Compose UI tests** for the primary interaction path only.
6. **Add screenshot tests** for design-system components and each screen (light/dark).
7. **Wire gates**: `test`, `lint`, `detekt`, `ktlint`, `koverVerify`, `verifyRoborazzi` in one `./gradlew check`.
8. **Track flakiness**: rerun failed tests once in CI, but record and fix every flake within a sprint.

## Patterns

✅ **MainDispatcherRule + Turbine**
```kotlin
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(dispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

class HomeViewModelTest {
    @get:Rule val dispatcherRule = MainDispatcherRule()
    private val repository = FakeArticleRepository()

    @Test
    fun `uiState emits Ready when repository returns articles`() = runTest {
        repository.emit(listOf(article("1"), article("2")))
        val viewModel = HomeViewModel(ObserveArticlesUseCase(repository), repository)

        viewModel.uiState.test {
            assertThat(awaitItem().content).isInstanceOf(ArticlesContent.Loading::class.java)
            val ready = awaitItem().content as ArticlesContent.Ready
            assertThat(ready.items).hasSize(2)
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `uiState emits Failed when repository throws`() = runTest {
        repository.failWith(AppError.Offline)
        // ...
    }
}
```

✅ **Fake over mock**
```kotlin
class FakeArticleRepository : ArticleRepository {
    private val flow = MutableSharedFlow<List<Article>>(replay = 1)
    var refreshResult: Outcome<Unit> = Outcome.Success(Unit)

    override fun observeArticles(): Flow<List<Article>> = flow
    override suspend fun refresh(): Outcome<Unit> = refreshResult
    suspend fun emit(items: List<Article>) = flow.emit(items)
}
```

✅ **Room integration test**
```kotlin
@RunWith(AndroidJUnit4::class)
class ArticleDaoTest {
    private lateinit var db: AppDatabase
    private lateinit var dao: ArticleDao

    @Before fun setUp() {
        db = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(), AppDatabase::class.java
        ).allowMainThreadQueries().build()
        dao = db.articleDao()
    }
    @After fun tearDown() = db.close()

    @Test fun upsert_replacesExistingRow() = runTest {
        dao.upsertAll(listOf(entity(id = "1", title = "old")))
        dao.upsertAll(listOf(entity(id = "1", title = "new")))
        assertThat(dao.observeAll().first().single().title).isEqualTo("new")
    }
}
```

✅ **Compose UI test**
```kotlin
@get:Rule val composeRule = createAndroidComposeRule<MainActivity>()

@Test fun clickingArticle_opensDetail() {
    composeRule.onNodeWithText("Kotlin 2.3 released").performClick()
    composeRule.onNodeWithTag("article_detail").assertIsDisplayed()
}
```

❌ **Don't**
```kotlin
@Test fun test1() {                       // meaningless name
    val vm = HomeViewModel(RealRepository(RetrofitClient.api))  // real network
    Thread.sleep(2000)                     // flaky by construction
    assertTrue(vm.items.value!!.isNotEmpty())
}
```

## Anti-patterns
- Mocking data classes or your own repositories when a fake is 10 lines.
- One test asserting 15 things — a failure tells you nothing.
- `verify(exactly = 3) { repo.load() }` — coupling the test to implementation.
- Instrumented tests for pure logic (slow, needs a device).
- Shared mutable state in `companion object` across tests.
- Chasing 100% coverage by testing getters; ignoring branch coverage on business rules.
- Screenshot tests with device-dependent rendering (use Paparazzi/Roborazzi, not a real device).

## Definition of Done
- [ ] Every ViewModel: loading, success, empty, error and retry paths tested.
- [ ] Fakes live in `core:testing` and are reused, not duplicated.
- [ ] Room migrations tested (`MigrationTestHelper`) for every schema bump.
- [ ] At least one Compose UI test per user-critical flow.
- [ ] Screenshot tests for all design-system components, light + dark + RTL.
- [ ] `./gradlew check` runs unit + lint + detekt + ktlint + coverage verification and is green.
- [ ] Coverage threshold enforced (start at 60% on changed modules, ratchet upward).
- [ ] Unit test suite finishes in < 3 minutes.

## References
- `references/test-strategy.md` — what to test at each level, fakes catalogue, flakiness playbook.
- `references/static-analysis.md` — detekt/ktlint/lint/Kover configuration and CI gates.
- Android testing docs: https://developer.android.com/training/testing

## ملخص عربي
هرم اختبار سليم: أغلبه وحدات على الـ JVM، ثم تكامل، وقليل من اختبارات الواجهة. اختبر السلوك لا
التفاصيل الداخلية، واستخدم fakes بدل mocks لواجهاتك. كل اختبار حتمي: dispatcher اختباري، ساعة
ثابتة، بلا `Thread.sleep` وبلا شبكة حقيقية. أضف اختبارات لقطات الشاشة لمكوّنات نظام التصميم،
واختبارات هجرة Room. البوابة النهائية: `./gradlew check` خضراء في CI.

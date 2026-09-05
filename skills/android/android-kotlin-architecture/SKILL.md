---
name: android-kotlin-architecture
description: >-
  Designs and reviews Android app architecture in Kotlin: layered Clean Architecture, UDF with
  MVVM/MVI, repositories, use cases, Hilt dependency injection, Coroutines and Flow, offline-first
  caching and error handling. Use when the user mentions architecture, ViewModel, UiState,
  repository, use case, Hilt, Dagger, dependency injection, coroutines, Flow, StateFlow,
  offline-first, modularization, or asks how to structure Android code or fix a God-class ViewModel.
version: 1.0.0
license: MIT
category: android
tags: [android, kotlin, architecture, mvvm, mvi, hilt, coroutines, flow, clean-architecture]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "تصميم معمارية أندرويد نظيفة: طبقات، تدفق بيانات أحادي الاتجاه، Hilt، Coroutines/Flow، وعمل دون اتصال."
---

# Android Kotlin Architecture

You are a staff Android architect. You optimise for **testability, change isolation and predictable
state** — not for the fewest files.

## When to use
- Deciding layers, modules, and data flow for a new feature or app.
- Reviewing/refactoring ViewModels, repositories, DI graphs, threading.
- Introducing offline-first behaviour or a single source of truth.

## When NOT to use
- Composable/UI implementation details → `android-compose-ui`.
- Room schema and migrations → `android-room-database`.
- Build/module wiring → `android-project-bootstrap`.

## Non-negotiables
- **MUST** follow the layer rule: `UI → Domain → Data`. Dependencies point **inward only**; the domain layer is pure Kotlin with **zero Android imports**.
- **MUST** expose UI state as a single immutable `StateFlow<UiState>` per screen. **NEVER** expose `MutableStateFlow`, `LiveData` mutables, or multiple ad-hoc flags that can contradict each other.
- **MUST** model state as a sealed hierarchy or a data class with explicit `Loading/Success/Error/Empty`. **NEVER** `isLoading && data != null && error != null` ambiguity.
- **MUST** keep a **single source of truth** for each datum (usually the database), with the network as a refresh mechanism.
- **MUST** inject dispatchers (`@Dispatcher(IO)`) — **NEVER** hardcode `Dispatchers.IO` inside a class you want to test.
- **MUST** collect flows in the UI lifecycle-aware (`repeatOnLifecycle(STARTED)` / `collectAsStateWithLifecycle`).
- **NEVER** reference `Context`, `View`, `Activity`, `Fragment`, or Android framework types in ViewModels or domain code.
- **NEVER** let a `ViewModel` exceed ~200 lines or hold more than 5 collaborators — extract use cases.
- **NEVER** swallow exceptions; map them to a domain `Result` type.

## Version pins
| Component | Version |
|---|---|
| Kotlin | 2.3.x |
| Coroutines | 1.10.x |
| Hilt | 2.5x (latest stable) |
| Lifecycle / ViewModel | 2.10.x |
| Navigation (Compose) | 2.9.x+ / Navigation 3 for new apps |

## Workflow
1. **Map the feature**: screens → user intents → data needs → sources (network/db/prefs).
2. **Define domain models** (`core:model`) — pure data classes; no DTOs, no entities leaking out.
3. **Declare repository interfaces in `core:domain`**, implement them in `core:data`. Dependency inversion is the point.
4. **Write use cases** only when there is real logic (composition, business rules). A pass-through use case is noise.
5. **Design `UiState`** for each screen before writing the ViewModel. Every field must be renderable.
6. **Implement the ViewModel**: intents in (`fun onEvent(e: Event)`), one `StateFlow` out, side effects via `Channel`/`SharedFlow`.
7. **Wire Hilt**: `@HiltViewModel`, `@Module @InstallIn(SingletonComponent::class)` bindings, qualifiers for dispatchers.
8. **Handle errors** with a `Result<T>` wrapper and a mapper to user-facing messages.
9. **Write tests first for the ViewModel** (`Turbine` + fake repository) — see `android-testing-quality`.
10. **Record the decision** as an ADR in `docs/adr/`.

## Patterns

✅ **State + events + one-way flow**
```kotlin
data class HomeUiState(
    val items: ImmutableList<Article> = persistentListOf(),
    val isRefreshing: Boolean = false,
    val message: UiText? = null,
)

sealed interface HomeEvent {
    data object Refresh : HomeEvent
    data class Open(val id: String) : HomeEvent
}

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val observeArticles: ObserveArticlesUseCase,
    private val repository: ArticleRepository,
) : ViewModel() {

    val uiState: StateFlow<HomeUiState> = observeArticles()
        .map { HomeUiState(items = it.toImmutableList()) }
        .catch { emit(HomeUiState(message = UiText.of(R.string.error_generic))) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), HomeUiState())

    fun onEvent(event: HomeEvent) = when (event) {
        HomeEvent.Refresh -> viewModelScope.launch { repository.refresh() }
        is HomeEvent.Open -> { /* emit navigation effect */ }
    }
}
```

✅ **Offline-first repository (single source of truth)**
```kotlin
class OfflineFirstArticleRepository @Inject constructor(
    private val dao: ArticleDao,
    private val api: ArticleApi,
    @Dispatcher(IO) private val io: CoroutineDispatcher,
) : ArticleRepository {

    override fun observeArticles(): Flow<List<Article>> =
        dao.observeAll().map { entities -> entities.map(ArticleEntity::toDomain) }

    override suspend fun refresh(): Result<Unit> = withContext(io) {
        runCatchingApi { api.fetchArticles() }
            .map { dtos -> dao.upsertAll(dtos.map(ArticleDto::toEntity)) }
    }
}
```

❌ **Don't**
```kotlin
class HomeViewModel(private val context: Context) : ViewModel() {   // Android in VM
    val isLoading = MutableLiveData(false)                          // mutable, exposed
    val error = MutableLiveData<String>()                           // contradictory states
    val data = MutableLiveData<List<Article>>()

    fun load() = viewModelScope.launch(Dispatchers.IO) {             // hardcoded dispatcher
        try { data.postValue(RetrofitClient.api.get()) }             // network from VM
        catch (e: Exception) { }                                     // swallowed
    }
}
```

## Anti-patterns
- **God ViewModel** doing networking, mapping, validation and navigation.
- **Leaky DTOs**: Retrofit/Room models used as UI models — every schema change breaks the UI.
- `GlobalScope.launch` — leaks work past the screen's lifetime; always use a scoped coroutine.
- `runBlocking` on the main thread.
- Singleton `object Repository` holding mutable state — untestable, race-prone.
- Passing `Flow` down into Composables and collecting without lifecycle awareness.
- Use cases that only call `repository.x()` one-to-one for all 30 methods.
- Using `SharedFlow(replay = 1)` for state (use `StateFlow`) or `StateFlow` for one-shot effects (use `Channel`).

## Definition of Done
- [ ] Domain module compiles as a **pure Kotlin (JVM) module** with no Android dependency.
- [ ] Each screen has exactly one `StateFlow<UiState>`; impossible states are unrepresentable.
- [ ] All dispatchers injected; no framework types in ViewModel/domain.
- [ ] Repositories return `Result`/sealed errors, never throw raw exceptions to the UI.
- [ ] Offline path verified: airplane mode still renders cached data.
- [ ] Configuration change and process death preserve state (`SavedStateHandle`).
- [ ] ViewModel unit tests cover loading, success, empty, error, retry.
- [ ] ADR written for every non-obvious decision.

## References
- `references/state-management.md` — UiState modelling, effects, SavedStateHandle, pagination.
- `references/di-and-threading.md` — Hilt modules, qualifiers, scopes, dispatcher testing.
- `references/error-handling.md` — Result type, mapping, retry/backoff, UiText.
- Official guide to app architecture: https://developer.android.com/topic/architecture

## ملخص عربي
معمارية نظيفة بثلاث طبقات: الواجهة تعتمد على المجال، والمجال لا يعرف أندرويد إطلاقًا، والبيانات
تنفّذ واجهات المجال. لكل شاشة حالة واحدة غير قابلة للتغيير `StateFlow<UiState>` وأحداث تدخل من
الواجهة. قاعدة البيانات هي المصدر الوحيد للحقيقة والشبكة مجرد تحديث. تُحقن الـ dispatchers ولا
تُكتب داخل الأصناف، وتُغلَّف الأخطاء في `Result`. الممنوعات: ViewModel عملاق، تسريب DTO للواجهة،
`GlobalScope`، وابتلاع الاستثناءات.

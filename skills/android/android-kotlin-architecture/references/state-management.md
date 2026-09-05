# State management — reference

## 1. Choosing the state shape

| Situation | Shape |
|---|---|
| Screen with independent sub-parts that all render | `data class UiState(...)` with defaults |
| Screen with mutually exclusive phases | `sealed interface UiState { Loading; Success(data); Error(cause); Empty }` |
| Both (common) | `data class UiState(val content: Content, val isRefreshing: Boolean, ...)` where `Content` is sealed |

**Rule:** if two fields can never be true at once, they belong in a sealed type.

```kotlin
sealed interface ArticlesContent {
    data object Loading : ArticlesContent
    data object Empty : ArticlesContent
    data class Ready(val items: ImmutableList<Article>) : ArticlesContent
    data class Failed(val reason: ErrorReason) : ArticlesContent
}

data class ArticlesUiState(
    val content: ArticlesContent = ArticlesContent.Loading,
    val isRefreshing: Boolean = false,
    val snackbar: UiText? = null,
)
```

Use `kotlinx.collections.immutable` (`ImmutableList`) so Compose can treat state as stable.

## 2. Events in, effects out

```kotlin
// in: plain function, one entry point
fun onEvent(event: HomeEvent)

// out (one-shot: navigation, toasts, dialogs dismissal)
private val _effects = Channel<HomeEffect>(Channel.BUFFERED)
val effects: Flow<HomeEffect> = _effects.receiveAsFlow()
```

Never model navigation as state (`shouldNavigate: Boolean`) — it re-fires on rotation.

## 3. `stateIn` and subscription timing

```kotlin
.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5_000), // survives config change, stops in background
    initialValue = HomeUiState(),
)
```
`5_000` ms is the standard grace window for rotation. Use `SharingStarted.Eagerly` only for
cheap, always-needed streams.

## 4. Combining multiple sources

```kotlin
val uiState = combine(
    userRepository.observeUser(),
    settingsRepository.observeSettings(),
    articleRepository.observeArticles(),
) { user, settings, articles ->
    HomeUiState(user = user, theme = settings.theme, content = articles.toContent())
}.stateIn(...)
```
Prefer one `combine` over several flows collected in the UI: it guarantees a consistent snapshot.

## 5. Process death & SavedStateHandle

```kotlin
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val savedState: SavedStateHandle,
    repo: SearchRepository,
) : ViewModel() {

    private val query = savedState.getStateFlow(KEY_QUERY, "")

    val uiState = query
        .debounce(300)
        .distinctUntilChanged()
        .flatMapLatest { q -> if (q.length < 2) flowOf(SearchUiState.Idle) else repo.search(q) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SearchUiState.Idle)

    fun onQueryChange(value: String) { savedState[KEY_QUERY] = value }

    private companion object { const val KEY_QUERY = "query" }
}
```

Store in `SavedStateHandle` only *user input and navigation arguments* — never large lists.

Test process death: `adb shell am kill com.company.app` while backgrounded, then reopen.

## 6. Pagination (Paging 3)

```kotlin
val articles: Flow<PagingData<Article>> = Pager(
    config = PagingConfig(pageSize = 20, prefetchDistance = 5, enablePlaceholders = false),
    remoteMediator = ArticleRemoteMediator(api, db),
    pagingSourceFactory = { dao.pagingSource() },
).flow.map { it.map(ArticleEntity::toDomain) }.cachedIn(viewModelScope)
```
`cachedIn` is mandatory — without it, rotation refetches everything.

## 7. State hoisting boundary

- ViewModel owns **business/screen state** (data, selection, submission status).
- Composable owns **ephemeral UI state** (scroll position, expanded/collapsed, text field cursor)
  via `rememberSaveable`.

## 8. Checklist
- [ ] No boolean pair that can encode an impossible state.
- [ ] One `StateFlow` per screen, exposed as read-only.
- [ ] Navigation/toasts are effects, not state.
- [ ] `WhileSubscribed(5_000)` unless justified.
- [ ] `cachedIn` on every paging flow.
- [ ] Rotation + process death tested manually.

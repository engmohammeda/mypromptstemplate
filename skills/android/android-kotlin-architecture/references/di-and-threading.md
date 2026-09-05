# Dependency injection & threading — reference

## 1. Hilt module layout

```
core/network/di/NetworkModule.kt       @InstallIn(SingletonComponent::class)
core/database/di/DatabaseModule.kt     @InstallIn(SingletonComponent::class)
core/data/di/RepositoryModule.kt       @Binds interfaces → implementations
core/common/di/DispatchersModule.kt    qualifiers
```

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindArticleRepository(impl: OfflineFirstArticleRepository): ArticleRepository
}
```

Use `@Binds` (abstract) over `@Provides` whenever you are just mapping an interface to an
implementation — it generates less code.

## 2. Dispatcher qualifiers (never hardcode)

```kotlin
enum class AppDispatcher { Default, IO }

@Qualifier
@Retention(AnnotationRetention.RUNTIME)
annotation class Dispatcher(val dispatcher: AppDispatcher)

@Module
@InstallIn(SingletonComponent::class)
object DispatchersModule {
    @Provides @Dispatcher(AppDispatcher.IO)
    fun providesIODispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides @Dispatcher(AppDispatcher.Default)
    fun providesDefaultDispatcher(): CoroutineDispatcher = Dispatchers.Default
}
```

In tests: inject `UnconfinedTestDispatcher()` / `StandardTestDispatcher(scheduler)`.

## 3. Scopes

| Scope | Use for |
|---|---|
| `SingletonComponent` | Database, Retrofit, DataStore, repositories |
| `ViewModelComponent` (`@ViewModelScoped`) | Per-screen caches, form validators |
| `ActivityRetainedComponent` | State shared across a navigation graph |
| `@ApplicationContext` | The only Context you may inject |

**Never** `@Singleton` something that holds mutable per-user state without a clear reset on logout.

## 4. Application-scoped work

```kotlin
@Retention(AnnotationRetention.RUNTIME) @Qualifier annotation class ApplicationScope

@Provides @Singleton @ApplicationScope
fun providesAppScope(@Dispatcher(Default) dispatcher: CoroutineDispatcher): CoroutineScope =
    CoroutineScope(SupervisorJob() + dispatcher)
```
Use it for "must finish even if the screen dies" work (e.g. sync a like). Everything else uses
`viewModelScope`. `GlobalScope` is banned.

## 5. Structured concurrency rules

- Every `launch` must be in a scope tied to a lifecycle.
- Use `supervisorScope` when sibling failures must not cancel each other.
- `withContext(io)` for blocking IO; suspend functions must be **main-safe** (callable from Main).
- Cancellation is cooperative: check `ensureActive()` in long loops; never catch
  `CancellationException` without rethrowing.

```kotlin
try { doWork() }
catch (e: CancellationException) { throw e }        // MUST rethrow
catch (e: Exception) { logger.e(e) }
```

## 6. Flow operators you should use (and the traps)

| Need | Operator | Trap |
|---|---|---|
| Latest search query wins | `flatMapLatest` | `flatMapConcat` queues stale requests |
| Drop duplicate emissions | `distinctUntilChanged` | forgetting it causes recomposition storms |
| Debounce typing | `debounce(300)` | debouncing a click stream hides taps |
| Hot state | `stateIn` | `shareIn` for events, not state |
| Retry network | `retryWhen { cause, attempt -> ... delay(backoff) }` | infinite retry loops |
| Combine sources | `combine` | `zip` waits for both — usually wrong here |

## 7. WorkManager with Hilt

```kotlin
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val repository: ArticleRepository,
) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result =
        repository.refresh().fold(onSuccess = { Result.success() }, onFailure = { Result.retry() })
}
```
Constraints: `NetworkType.CONNECTED`, `setBackoffCriteria(EXPONENTIAL, 30, SECONDS)`,
unique work with `ExistingWorkPolicy.KEEP`.

## 8. Checklist
- [ ] Zero `Dispatchers.X` literals outside DI modules.
- [ ] No `GlobalScope`, no `runBlocking` in production code.
- [ ] `CancellationException` always rethrown.
- [ ] Every suspend function is main-safe.
- [ ] Singleton graph resets on logout.

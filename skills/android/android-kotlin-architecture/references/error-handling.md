# Error handling — reference

## 1. A domain Result type

```kotlin
sealed interface Outcome<out T> {
    data class Success<T>(val data: T) : Outcome<T>
    data class Failure(val error: AppError) : Outcome<Nothing>
}

sealed interface AppError {
    data object Offline : AppError
    data object Timeout : AppError
    data class Http(val code: Int, val serverMessage: String?) : AppError
    data class Serialization(val cause: Throwable) : AppError
    data class Storage(val cause: Throwable) : AppError
    data class Unknown(val cause: Throwable) : AppError
}
```

Why not `kotlin.Result`? It boxes, discourages exhaustive `when`, and cannot be used as a
return type in some positions. A sealed hierarchy forces the UI to handle every case.

## 2. Mapping at the boundary

```kotlin
suspend fun <T> apiCall(block: suspend () -> T): Outcome<T> = try {
    Outcome.Success(block())
} catch (e: CancellationException) {
    throw e
} catch (e: UnknownHostException) {
    Outcome.Failure(AppError.Offline)
} catch (e: SocketTimeoutException) {
    Outcome.Failure(AppError.Timeout)
} catch (e: HttpException) {
    Outcome.Failure(AppError.Http(e.code(), e.response()?.errorBody()?.string()))
} catch (e: SerializationException) {
    Outcome.Failure(AppError.Serialization(e))
} catch (e: Throwable) {
    Outcome.Failure(AppError.Unknown(e))
}
```
Exceptions are converted **once**, at the data-source boundary. Above that layer, no `try/catch`.

## 3. Errors are UI text, resolved late

```kotlin
sealed interface UiText {
    data class Raw(val value: String) : UiText
    data class Res(@StringRes val id: Int, val args: List<Any> = emptyList()) : UiText
}

fun AppError.toUiText(): UiText = when (this) {
    AppError.Offline -> UiText.Res(R.string.error_offline)
    AppError.Timeout -> UiText.Res(R.string.error_timeout)
    is AppError.Http -> when (code) {
        401 -> UiText.Res(R.string.error_session_expired)
        in 500..599 -> UiText.Res(R.string.error_server)
        else -> UiText.Res(R.string.error_generic)
    }
    else -> UiText.Res(R.string.error_generic)
}
```
ViewModels must not build user-facing strings — no `Context` there.

## 4. Retry policy

| Error | Behaviour |
|---|---|
| `Offline` | Show cached data + persistent "offline" banner; auto-retry on connectivity regain |
| `Timeout` / 5xx | Exponential backoff, max 3 attempts, jitter |
| 4xx (except 401/429) | Do not retry — it is a bug or bad input |
| 401 | Refresh token once, then force logout |
| 429 | Honour `Retry-After` header |

```kotlin
fun <T> Flow<T>.retryWithBackoff(max: Int = 3, base: Long = 500) = retryWhen { cause, attempt ->
    val retryable = cause is IOException || (cause as? HttpException)?.code() in 500..599
    if (retryable && attempt < max) { delay(base * (1L shl attempt.toInt()) + Random.nextLong(200)); true }
    else false
}
```

## 5. What the user must never see
- Stack traces, `NullPointerException`, raw JSON, SQL messages.
- A spinner with no timeout.
- A silent failure (empty screen with no explanation and no retry action).

Every error state MUST offer: a plain-language cause, and one primary recovery action.

## 6. Crash reporting
- Log non-fatal `AppError.Unknown` to Crashlytics/Sentry with breadcrumbs, **never** with PII.
- Set `firebase_crashlytics_collection_enabled=false` until the user consents.
- Symbolicate release builds: upload the R8 mapping file in CI (`uploadCrashlyticsMappingFileRelease`).

## 7. Checklist
- [ ] Exceptions caught exactly once, at the data boundary.
- [ ] `CancellationException` rethrown everywhere.
- [ ] Every `AppError` maps to a localized string and a recovery action.
- [ ] Retry has a bound and backoff with jitter.
- [ ] Offline shows cached content, not an error screen.
- [ ] Mapping file uploaded for release builds.

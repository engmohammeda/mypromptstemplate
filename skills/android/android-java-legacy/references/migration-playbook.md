# Legacy migration playbook — reference

## A. Ordered upgrade path (never skip a stage)

| Stage | Goal | Exit criterion |
|---|---|---|
| 0 | Freeze: CI builds the current app, tests recorded | green baseline |
| 1 | Gradle wrapper + AGP up one major at a time | `assembleDebug` green |
| 2 | AndroidX migration, jetifier off | no `android.support` imports |
| 3 | ViewBinding everywhere touched | no `findViewById` in new/edited code |
| 4 | Deprecated API removal | lint deprecation count → 0 |
| 5 | Architecture seams (DI, repositories) | ViewModels unit-testable |
| 6 | Kotlin adoption, file by file | new code 100% Kotlin |
| 7 | targetSdk to current requirement | Play upload accepted |
| 8 | Compose interop for new screens | `ComposeView` in existing fragments |

## B. targetSdk behaviour changes that break old apps

| Target | Break | Fix |
|---|---|---|
| 29 | Scoped storage | MediaStore / SAF, drop `WRITE_EXTERNAL_STORAGE` |
| 30 | Package visibility | `<queries>` in the manifest |
| 31 | `PendingIntent` mutability required | add `FLAG_IMMUTABLE`/`FLAG_MUTABLE` |
| 31 | Exact alarms restricted | `SCHEDULE_EXACT_ALARM` or use WorkManager |
| 31 | `android:exported` mandatory | declare on every activity/service/receiver with an intent filter |
| 33 | Notification runtime permission | request `POST_NOTIFICATIONS` |
| 33 | Granular media permissions | `READ_MEDIA_IMAGES/VIDEO/AUDIO` |
| 34 | Foreground service types mandatory | `android:foregroundServiceType` + matching permission |
| 34 | Non-dismissable notifications changed | review ongoing notifications |
| 35 | Edge-to-edge enforced | handle insets; `Scaffold`/`windowInsetsPadding` |
| 35 | Non-SDK interface restrictions tightened | remove reflection into hidden APIs |
| 36 | Full-screen intent needs `USE_FULL_SCREEN_INTENT` | request or redesign the alert |
| 36 | Predictive back default | `enableOnBackInvokedCallback="true"` + `OnBackPressedCallback` |

Test each with: `adb shell am compat enable <CHANGE_ID> <package>` (compat framework) before flipping targetSdk.

## C. Java → Kotlin conversion rules

1. **Annotate first**: add `@Nullable`/`@NonNull` to the Java file's public API, or Kotlin gets
   platform types (`String!`) and NPEs move to runtime.
2. **Convert leaves first**: models → utils → data sources → ViewModels → UI.
3. **One file per PR**, no behaviour change in the same commit.
4. **Post-conversion cleanup checklist**:
   - Replace `!!` with `?.`/`requireNotNull(x) { "reason" }`.
   - `companion object` constants → top-level `const val` or keep `@JvmField` for Java callers.
   - Add `@JvmStatic`, `@JvmOverloads`, `@JvmName` where Java still calls in.
   - Convert getters/setters to properties.
   - Replace `if (x != null)` chains with `?.let`, `?:`.
   - Data classes for POJOs; `sealed` for type codes / `int` constants.
   - Replace `Utils` static classes with extension functions.
5. **Verify**: the module still compiles for Java callers; run the full test suite.

## D. Killing memory leaks (add LeakCanary in debug)

| Leak | Cause | Fix |
|---|---|---|
| Activity retained | static field, singleton listener, non-static inner class | `WeakReference`, unregister in `onDestroy`, use `applicationContext` |
| Fragment view retained | binding not nulled in `onDestroyView` | null it |
| Handler leak | delayed message holding the Activity | `removeCallbacksAndMessages(null)` |
| RxJava | undisposed subscription | `CompositeDisposable.clear()` in `onStop` |
| Listener leak | registered but never unregistered | pair every register with an unregister |

## E. Testing a codebase with no tests
1. Write **characterization tests**: assert current behaviour, even if it is wrong.
2. Use Robolectric for Activity/Fragment logic without a device.
3. Extract a pure function from the middle of a big method → test it → keep going (Sprout Method).
4. Introduce an interface at the boundary you cannot control (network, clock, storage), then fake it.
5. Target: 60% coverage on the modules you actively change; do not chase global coverage.

## F. Mixed-language module hygiene
- One source root: `src/main/java` can hold both `.java` and `.kt`; do not split into `src/main/kotlin` mid-migration.
- Keep `kotlin-stdlib` in the version catalog, never per-module versions.
- Enable `-Xjsr305=strict` so JSR-305 nullability annotations are enforced.
- Migrate annotation processors to KSP where the library supports it; KAPT is the slowest part of a legacy build.

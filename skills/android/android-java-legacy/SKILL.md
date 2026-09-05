---
name: android-java-legacy
description: >-
  Maintains, modernizes and incrementally migrates legacy Java Android codebases: AsyncTask and
  Loader removal, findViewById to ViewBinding, support library to AndroidX, Activity/Fragment
  lifecycle bugs, RxJava interop, and safe Java-to-Kotlin conversion. Use when the user works with
  Java Android code, mentions AsyncTask, findViewById, ButterKnife, support-v4, Loader, legacy app,
  old codebase, targetSdk upgrade of an old app, or asks to convert Java to Kotlin.
version: 1.0.0
license: MIT
category: android
tags: [android, java, legacy, migration, kotlin, androidx, refactoring]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "صيانة وتحديث مشاريع أندرويد بلغة جافا والهجرة التدريجية الآمنة إلى AndroidX وكوتلن."
---

# Android Java Legacy & Migration

You are the engineer who keeps a 6-year-old, 300k-line Java app shipping — while moving it forward
**without a rewrite**.

## When to use
- The codebase is Java (or mixed) and must keep shipping.
- Raising `targetSdk` on an old app to meet Play requirements.
- Removing deprecated APIs; introducing Kotlin file-by-file.

## When NOT to use
- Greenfield projects → `android-project-bootstrap` + `android-kotlin-architecture` (Kotlin-first).

## Non-negotiables
- **MUST** migrate incrementally behind green tests. **NEVER** propose a big-bang rewrite.
- **MUST** run/create a characterization test before changing behaviour you do not fully understand.
- **MUST** complete the AndroidX migration (`android.support.*` is dead) before anything else.
- **MUST** remove `AsyncTask`, `Loader`, `startActivityForResult`, `onActivityResult`, `setRetainInstance`, `LocalBroadcastManager` — all deprecated/removed.
- **MUST** keep Java and Kotlin interop safe: annotate Java with `@Nullable`/`@NonNull` **before** converting callers to Kotlin.
- **MUST** raise `targetSdk` one API level at a time, reading the behaviour-change list for each.
- **NEVER** convert a whole package with the IDE converter and commit without reviewing every file — the converter produces `!!`, wrong nullability, and non-idiomatic code.
- **NEVER** leave a converted file with platform types (`String!`) in a public API.

## Version pins
| Component | Version |
|---|---|
| Java language level | 17 (with desugaring for `java.time` on old minSdk) |
| AGP | 9.1.x |
| AndroidX AppCompat | 1.7.x |
| Kotlin (for mixed modules) | 2.3.x |
| targetSdk goal | 36 (Play requirement since 2026-08-31) |

## Workflow
1. **Assess**: run `./gradlew lint`, count deprecations, list `android.support` imports, measure test coverage, record build time.
2. **Stabilise the build**: upgrade Gradle/AGP step-by-step (7.x → 8.x → 9.x), fix one error class at a time.
3. **AndroidX**: `Refactor → Migrate to AndroidX` (Android Studio), then fix `jetifier`-dependent libs and remove `android.enableJetifier=true`.
4. **Kill deprecated APIs** in this order: `AsyncTask` → `ExecutorService`/coroutines; `startActivityForResult` → `ActivityResultContracts`; `Loader` → `ViewModel` + repository; `findViewById` → **ViewBinding**; `LocalBroadcastManager` → `SharedFlow`/`LiveData`.
5. **Introduce Kotlin** on the leaf edges (models, utils, new features). Add `kotlin-android` (or rely on AGP 9 built-in Kotlin) and convert **one file per PR**.
6. **Add seams for tests**: extract interfaces, remove static singletons, inject dependencies via constructor.
7. **Raise `targetSdk`** incrementally, testing each behaviour change (permissions, background limits, scoped storage, exact alarms, foreground service types, predictive back, edge-to-edge on 35+).
8. **Track progress** in `docs/migration-status.md` (files converted / deprecations remaining / coverage).

## Patterns

✅ **AsyncTask → Executor (pure Java, no Kotlin needed yet)**
```java
public class ArticleLoader {
    private final ExecutorService io = Executors.newFixedThreadPool(4);
    private final Handler main = new Handler(Looper.getMainLooper());

    public void load(@NonNull Callback<List<Article>> callback) {
        io.execute(() -> {
            try {
                List<Article> result = repository.fetch();
                main.post(() -> callback.onSuccess(result));
            } catch (IOException e) {
                main.post(() -> callback.onError(e));
            }
        });
    }
}
```

✅ **startActivityForResult → ActivityResultContracts**
```java
private final ActivityResultLauncher<String> pickImage =
    registerForActivityResult(new ActivityResultContracts.GetContent(), uri -> {
        if (uri != null) viewModel.onImagePicked(uri);
    });
// launch: pickImage.launch("image/*");
```

✅ **findViewById → ViewBinding**
```java
public class ProfileFragment extends Fragment {
    private FragmentProfileBinding binding;

    @Override public View onCreateView(LayoutInflater i, ViewGroup c, Bundle s) {
        binding = FragmentProfileBinding.inflate(i, c, false);
        return binding.getRoot();
    }
    @Override public void onDestroyView() {   // MUST null it out — otherwise leak
        super.onDestroyView();
        binding = null;
    }
}
```

✅ **Nullability contract before converting callers**
```java
@NonNull public String getTitle() { return title; }
@Nullable public User getCachedUser() { return cache.get(); }
```

❌ **Don't**
```java
new AsyncTask<Void, Void, String>() {           // deprecated, leaks the Activity
    protected String doInBackground(Void... v) { return api.get(); }
    protected void onPostExecute(String r) { textView.setText(r); }  // may be dead
}.execute();
```

## Anti-patterns
- Static `Context` / `Activity` fields ("just for convenience") — guaranteed leak.
- `Fragment` constructors with arguments instead of `Bundle` args → crash on restore.
- Business logic in `Activity.onCreate` (500-line activities).
- `android.enableJetifier=true` kept forever — it slows every build.
- `Thread` + `runOnUiThread` sprinkled everywhere with no cancellation.
- Converting to Kotlin while simultaneously changing behaviour in the same PR.
- Suppressing lint (`@SuppressLint`) instead of fixing the cause.

## Definition of Done
- [ ] Zero `android.support.*` imports; jetifier disabled.
- [ ] Zero usages of `AsyncTask`, `Loader`, `onActivityResult`, `LocalBroadcastManager`.
- [ ] `findViewById` replaced with ViewBinding in all touched screens.
- [ ] All public Java APIs annotated `@Nullable`/`@NonNull`.
- [ ] `targetSdk` at the Play-required level; each behaviour change verified on a device.
- [ ] LeakCanary shows zero leaks in the main flows.
- [ ] Build + lint + tests green; migration status doc updated.

## References
- `references/migration-playbook.md` — ordered upgrade path, targetSdk behaviour changes, Java→Kotlin conversion rules.
- Android behaviour changes: https://developer.android.com/about/versions
- AndroidX migration: https://developer.android.com/jetpack/androidx/migrate

## ملخص عربي
هجرة تدريجية آمنة لمشاريع جافا القديمة: أولًا استقرار البناء وترقية Gradle/AGP، ثم AndroidX،
ثم إزالة الواجهات المهجورة (AsyncTask، Loader، onActivityResult، findViewById)، ثم إدخال كوتلن
ملفًا ملفًا مع توثيق قابلية القيم الفارغة، وأخيرًا رفع `targetSdk` درجة درجة مع اختبار كل تغيير
سلوكي. ممنوع إعادة الكتابة الشاملة أو دمج تحويل اللغة مع تغيير السلوك في نفس الـ PR.

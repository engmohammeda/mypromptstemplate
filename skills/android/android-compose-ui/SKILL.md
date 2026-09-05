---
name: android-compose-ui
description: >-
  Implements and reviews Jetpack Compose screens: state hoisting, stateless composables, Material 3
  theming, adaptive layouts, accessibility, animation and recomposition performance. Use when the
  user mentions Compose, @Composable, remember, recomposition, Material 3, MaterialTheme, Modifier,
  LazyColumn, Scaffold, previews, Compose navigation, or asks to build, restyle, or fix an Android
  screen, or to migrate XML layouts to Compose.
version: 1.0.0
license: MIT
category: android
tags: [android, compose, ui, material3, accessibility, performance]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "بناء واجهات Jetpack Compose: رفع الحالة، مكوّنات بلا حالة، Material 3، تكيّف الشاشات، وإتاحة وأداء."
---

# Android Compose UI

You are a senior Compose engineer. Every screen you write is **stateless, previewable, accessible,
and recomposition-cheap**.

## When to use
- Building or refactoring any Compose screen or component.
- Migrating XML/Views to Compose.
- Fixing jank, over-recomposition, or theming inconsistency.

## When NOT to use
- Visual language, tokens, spacing scale → `ui-design-system`.
- Flow/journey design → `ux-flow-architect`.
- ViewModel/state architecture → `android-kotlin-architecture`.

## Non-negotiables
- **MUST** split every screen into a stateful `XRoute` (reads ViewModel) and a stateless `XScreen(state, onEvent)` that is fully previewable.
- **MUST** hoist state: a composable that owns state it does not need is a bug.
- **MUST** pass `Modifier` as the **first optional parameter**, defaulting to `Modifier`, and apply it to the root element only.
- **MUST** read all colors/type/shape from `MaterialTheme` (or the app's token object). **NEVER** hardcode `Color(0xFF...)`, `16.sp`, or `RoundedCornerShape(8.dp)` inline in feature code.
- **MUST** provide `contentDescription` for meaningful images/icons and `null` for decorative ones; minimum touch target **48dp**.
- **MUST** use `key` in `LazyColumn`/`LazyRow` items and `contentType` for heterogeneous lists.
- **MUST** collect state with `collectAsStateWithLifecycle()`, never `collectAsState()` for lifecycle-bound data.
- **NEVER** perform side effects (network, navigation, logging) directly in a composable body — use `LaunchedEffect`, `SideEffect`, `DisposableEffect`.
- **NEVER** pass a `ViewModel` into a child composable.
- **NEVER** use `Modifier.background()` before `clip()` when a shape is expected, or nest scrollable containers of the same axis.
- **NEVER** use unstable types (`List`, `Map`, lambdas capturing unstable state) in composable params when `ImmutableList`/`@Immutable` is available.

## Version pins
| Component | Version |
|---|---|
| Compose BOM | 2026.08.00 |
| Kotlin / compose compiler plugin | 2.3.x (must match) |
| Material 3 | via BOM |
| material3-adaptive | via BOM |
| Lifecycle runtime-compose | 2.10.x |

## Workflow
1. **Read the design tokens** from `core:designsystem`. If they don't exist, invoke `ui-design-system` first.
2. **Define `UiState` and `Event`** with the architecture skill; the UI never invents state.
3. **Write the stateless `Screen`** with `@Preview` variants: light, dark, RTL (Arabic), font scale 2.0, and small/large window sizes.
4. **Compose from small atoms** (`core:designsystem`) → molecules → screen. No 400-line composable.
5. **Add adaptive behaviour** with `WindowSizeClass` / `NavigationSuiteScaffold` for phone/foldable/tablet.
6. **Add accessibility semantics**: roles, `stateDescription`, merged/cleared semantics, focus order.
7. **Verify recomposition** with Layout Inspector recomposition counts and the compiler metrics report.
8. **Test**: Compose UI test for behaviour + Roborazzi/Paparazzi screenshot test for appearance.

## Patterns

✅ **Route / Screen split**
```kotlin
@Composable
fun HomeRoute(
    onOpenArticle: (String) -> Unit,
    viewModel: HomeViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    HomeScreen(state = state, onEvent = viewModel::onEvent, onOpenArticle = onOpenArticle)
}

@Composable
fun HomeScreen(
    state: HomeUiState,
    onEvent: (HomeEvent) -> Unit,
    onOpenArticle: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    Scaffold(modifier = modifier, topBar = { HomeTopBar(onRefresh = { onEvent(HomeEvent.Refresh) }) }) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            items(items = state.items, key = { it.id }, contentType = { "article" }) { article ->
                ArticleCard(article = article, onClick = { onOpenArticle(article.id) })
            }
        }
    }
}

@Preview(name = "Light")
@Preview(name = "Dark", uiMode = UI_MODE_NIGHT_YES)
@Preview(name = "RTL", locale = "ar")
@Preview(name = "Large font", fontScale = 2.0f)
@Composable
private fun HomeScreenPreview(@PreviewParameter(HomeStateProvider::class) state: HomeUiState) {
    AppTheme { HomeScreen(state = state, onEvent = {}, onOpenArticle = {}) }
}
```

✅ **Defer state reads to the smallest scope (lambda modifiers)**
```kotlin
// Recomposes only the graphics layer, not the whole tree
Box(Modifier.graphicsLayer { alpha = scrollAlpha })
Text("Total", Modifier.offset { IntOffset(0, offsetY.roundToInt()) })
```

❌ **Don't**
```kotlin
@Composable
fun Home(viewModel: HomeViewModel) {          // VM passed down, not previewable
    val items = viewModel.repo.load()          // side effect in composition
    Column(Modifier.verticalScroll(rememberScrollState())) {
        items.forEach { ArticleCard(it) }      // no lazy list, no keys
    }
    Text("Title", color = Color(0xFF1A73E8), fontSize = 18.sp)  // hardcoded design
}
```

## Anti-patterns
- `Column { verticalScroll }` holding hundreds of items instead of `LazyColumn`.
- `remember` without keys around values derived from parameters → stale UI. Use `derivedStateOf`/`remember(key)`.
- Reading a frequently-changing state (scroll offset, animation) at the top of a screen — hoists recomposition to the root.
- `LaunchedEffect(Unit)` for something that must re-run when a parameter changes.
- Building strings with `stringResource` inside a loop body of a lazy list on every frame.
- Using `Spacer` chains instead of `Arrangement.spacedBy`.
- Custom colors object bypassing `MaterialTheme` → dark mode breaks.
- Applying `Modifier` parameter to an inner child instead of the root (breaks caller expectations).

## Definition of Done
- [ ] Screen renders in previews: light, dark, RTL, fontScale 2.0, compact + expanded width.
- [ ] Zero hardcoded colors/dimensions/typography outside the design system module.
- [ ] All interactive elements ≥ 48dp and reachable by TalkBack in a logical order.
- [ ] Lazy lists use stable `key`s; scrolling holds 60/120fps on a mid-range device.
- [ ] Compose compiler metrics show no unexpected unstable parameters on hot composables.
- [ ] No side effects outside effect handlers.
- [ ] UI test covers the primary interaction; screenshot test covers light + dark.

## References
- `references/compose-performance.md` — stability, metrics, recomposition, Baseline Profiles hand-off.
- `references/compose-accessibility.md` — semantics, TalkBack, contrast, touch targets, RTL.
- `references/adaptive-layouts.md` — window size classes, foldables, list-detail, navigation suite.
- Compose performance docs: https://developer.android.com/develop/ui/compose/performance

## ملخص عربي
كل شاشة تُقسم إلى `Route` (يقرأ الـ ViewModel) و`Screen` بلا حالة قابل للمعاينة. تُرفع الحالة
للأعلى، ويُمرَّر `Modifier` كأول معامل اختياري ويُطبَّق على الجذر فقط. كل الألوان والخطوط من
`MaterialTheme`، ولا قيم صلبة في كود الميزات. القوائم الطويلة `Lazy*` مع `key`. الإتاحة إلزامية:
وصف للمحتوى، هدف لمس 48dp، دعم RTL وتكبير الخط. لا آثار جانبية داخل جسم الـ composable.

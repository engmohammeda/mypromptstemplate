# Compose performance — reference

## 1. The three phases
`Composition` (what) → `Layout` (where) → `Drawing` (how). Push state reads as **late** as possible:

| Read location | Cost when the value changes |
|---|---|
| Composable body | recompose subtree |
| Lambda modifier (`Modifier.offset { }`, `graphicsLayer { }`) | skip composition, only layout/draw |
| `drawBehind { }` | only draw |

```kotlin
// ❌ recomposes on every scroll pixel
Box(Modifier.alpha(1f - scrollState.value / 500f))
// ✅ only redraws
Box(Modifier.graphicsLayer { alpha = 1f - scrollState.value / 500f })
```

## 2. Stability rules
A type is **stable** if: it is immutable, or Compose can be notified of changes (`MutableState`).

| Type | Stable? | Fix |
|---|---|---|
| `data class` with `val` primitives | ✅ | — |
| `List<T>`, `Map<K,V>`, `Set<T>` | ❌ (interface, could be mutable) | `ImmutableList` from kotlinx.collections.immutable, or `@Immutable` |
| Class from another module without the Compose compiler | ❌ | mark `@Stable`/`@Immutable`, or add a stability config file |
| Lambdas capturing unstable values | ❌ | pass method references (`viewModel::onEvent`) |

Stability config file (`compose_compiler_config.conf`) for third-party types:
```
java.time.LocalDate
com.thirdparty.model.*
```
```kotlin
composeCompiler {
    stabilityConfigurationFile = rootProject.layout.projectDirectory.file("compose_compiler_config.conf")
    reportsDestination = layout.buildDirectory.dir("compose_compiler")
    metricsDestination = layout.buildDirectory.dir("compose_compiler")
}
```

Run and read the report:
```bash
./gradlew :app:assembleRelease
# build/compose_compiler/*-composables.txt → look for "restartable but not skippable"
```
Goal: every hot composable is **restartable + skippable**.

## 3. Lazy list rules
```kotlin
LazyColumn {
    items(
        items = state.items,
        key = { it.id },                 // stable identity → reuse + animations
        contentType = { it.kind },       // reuse pools per type
    ) { item -> Row(item) }
}
```
- Never use the index as a key when the list can reorder.
- Avoid `Modifier.animateItem()` on lists of > 500 items without measurement.
- Do not put a `LazyColumn` inside a vertically scrollable `Column` — it crashes or loads everything.
- Pre-size images (`Modifier.size`) so layout does not jump.

## 4. `remember` and `derivedStateOf`
```kotlin
// ✅ recomposes only when the boolean flips, not on every scroll item change
val showButton by remember { derivedStateOf { listState.firstVisibleItemIndex > 3 } }

// ✅ keyed remember: recomputed when `query` changes
val filtered = remember(query, items) { items.filter { it.title.contains(query, true) } }
```
Rule: `derivedStateOf` when *many inputs → few outputs*; keyed `remember` for pure derivation.

## 5. Common jank sources
| Symptom | Cause | Fix |
|---|---|---|
| Scroll stutter on first launch | JIT / no profile | Baseline Profile (see `android-performance`) |
| Whole screen recomposes on typing | state read at root | hoist the text field state into its own composable |
| Image pop-in | no placeholder/size | Coil `placeholder` + fixed aspect ratio |
| Slow first frame | heavy work in composition | move to ViewModel/`LaunchedEffect` |
| Repeated recomposition loops | writing state during composition | move the write into an effect |

## 6. Measuring
- **Layout Inspector** → recomposition counts (skipped vs recomposed).
- **Macrobenchmark** `FrameTimingMetric` for P50/P90/P99 frame duration.
- **Perfetto** trace for > 16ms frames (or > 8ms at 120Hz).

Budget: P99 frame < 16 ms; zero frozen frames (> 700 ms) during a scroll of 100 items.

## 7. Checklist
- [ ] Compiler metrics: no unexpected unstable params on hot paths.
- [ ] All lazy items keyed.
- [ ] Animated/scroll-driven values read in lambda modifiers.
- [ ] `derivedStateOf` used for scroll-derived booleans.
- [ ] Macrobenchmark scroll test recorded and within budget.

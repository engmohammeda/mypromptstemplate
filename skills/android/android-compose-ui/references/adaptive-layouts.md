# Adaptive layouts — reference

## 1. Window size classes (the only breakpoints you need)

| Class | Width | Typical device | Layout |
|---|---|---|---|
| Compact | < 600dp | phone portrait | single pane, bottom navigation |
| Medium | 600–839dp | foldable open, small tablet, phone landscape | navigation rail, optional two-pane |
| Expanded | ≥ 840dp | tablet, desktop, large foldable | list-detail / supporting pane, navigation drawer |

Height classes matter for one thing: compact height (landscape phone) → avoid vertical wizards,
use a horizontal layout and keep the CTA visible.

```kotlin
val windowSize = currentWindowAdaptiveInfo().windowSizeClass
when (windowSize.windowWidthSizeClass) {
    WindowWidthSizeClass.COMPACT -> SinglePane()
    else -> ListDetail()
}
```

## 2. Navigation that adapts automatically

```kotlin
NavigationSuiteScaffold(
    navigationSuiteItems = {
        destinations.forEach { dest ->
            item(
                selected = dest == current,
                onClick = { onSelect(dest) },
                icon = { Icon(dest.icon, contentDescription = null) },
                label = { Text(stringResource(dest.label)) },
            )
        }
    },
) { content() }
```
It renders a bottom bar (compact), rail (medium) or permanent drawer (expanded) for you.

## 3. Canonical layouts
- **List-detail** — `ListDetailPaneScaffold` (mail, catalogs). On compact it degrades to navigation.
- **Supporting pane** — main content + secondary tools (editor + properties).
- **Feed** — responsive grid, `GridCells.Adaptive(minSize = 160.dp)`; never a fixed column count.

```kotlin
val navigator = rememberListDetailPaneScaffoldNavigator<String>()
ListDetailPaneScaffold(
    directive = navigator.scaffoldDirective,
    value = navigator.scaffoldValue,
    listPane = { AnimatedPane { ItemList(onClick = { navigator.navigateTo(ListDetailPaneScaffoldRole.Detail, it) }) } },
    detailPane = { AnimatedPane { Detail(navigator.currentDestination?.contentKey) } },
)
```

## 4. Foldables
- Use `WindowInfoTracker` / `currentWindowAdaptiveInfo().windowPosture` to detect a hinge.
- Table-top posture (half-open, horizontal hinge): media on top, controls below.
- Never place an interactive element under the fold/hinge occlusion bounds.
- Handle configuration changes without losing state — `rememberSaveable` + `SavedStateHandle`.

## 5. Insets & edge-to-edge (mandatory on API 35+)
```kotlin
enableEdgeToEdge()   // in onCreate, before setContent
Scaffold { padding -> Content(Modifier.padding(padding)) }
// or explicitly:
Modifier.windowInsetsPadding(WindowInsets.safeDrawing)
Modifier.imePadding()               // keyboard
Modifier.navigationBarsPadding()
```
`android:windowSoftInputMode="adjustResize"` for keyboard-aware screens.
Test with 3-button nav, gesture nav, and a display cutout.

## 6. Do / Don't

✅ Adaptive grid
```kotlin
LazyVerticalGrid(columns = GridCells.Adaptive(minSize = 160.dp))
```
❌ Device-type branching
```kotlin
if (isTablet) { /* ... */ }   // fails on foldables, split-screen, desktop windowing
```

Other bans:
- `Configuration.screenWidthDp` hardcoded thresholds scattered across files.
- Locking orientation (`android:screenOrientation="portrait"`) — breaks tablets, ChromeOS, and is penalised in Play's large-screen quality guidelines.
- Assuming the app owns the full display (split-screen, desktop windowing, XR).

## 7. Checklist
- [ ] Works in compact / medium / expanded previews and in split-screen.
- [ ] No orientation lock; rotation preserves state and scroll position.
- [ ] Edge-to-edge with correct insets on gesture and button navigation.
- [ ] Keyboard never covers the focused field.
- [ ] Foldable table-top and unfolded states verified in the emulator.

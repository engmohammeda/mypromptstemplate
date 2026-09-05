# Compose accessibility — reference (WCAG 2.2 AA + Android)

## 1. Hard requirements

| Rule | Value | How to verify |
|---|---|---|
| Touch target | ≥ 48×48 dp | Accessibility Scanner |
| Text contrast | ≥ 4.5:1 (normal), 3:1 (≥ 18.66sp bold / 24sp) | contrast checker on tokens |
| Non-text contrast (icons, borders, focus ring) | ≥ 3:1 | manual |
| Text scaling | usable at 200% font scale | `@Preview(fontScale = 2f)` |
| Layout scaling | usable at display size "largest" | device settings |
| Color alone conveys meaning | forbidden — add icon/text | review |
| Motion | respect "remove animations" setting | test with animations off |

## 2. Semantics API

```kotlin
Icon(
    imageVector = Icons.Default.Favorite,
    contentDescription = if (isFavorite) stringResource(R.string.remove_favorite)
                         else stringResource(R.string.add_favorite),
)

// Decorative only:
Image(painter = painterResource(R.drawable.bg_wave), contentDescription = null)

// Custom control with a role and state
Row(
    modifier = Modifier
        .toggleable(
            value = checked,
            role = Role.Checkbox,
            onValueChange = onCheckedChange,
        )
        .semantics {
            stateDescription = if (checked) enabledLabel else disabledLabel
        }
        .minimumInteractiveComponentSize(),
) { /* ... */ }
```

- `Modifier.semantics(mergeDescendants = true)` for a card that should be read as one item.
- `Modifier.clearAndSetSemantics { }` to replace a noisy subtree with one clean label.
- `Modifier.semantics { heading() }` for section titles so TalkBack users can jump.
- `LiveRegionMode.Polite` for async status text (e.g. "3 results found").
- `traversalIndex` / `isTraversalGroup` to fix reading order in overlapping layouts.

## 3. Never do
- `contentDescription = "image"` / `"button"` / the file name.
- A clickable `Box` of 24dp without `minimumInteractiveComponentSize()`.
- Text inside an image bitmap (unreadable, untranslatable, unscalable).
- Disabling the system font scale (`fontScale` overrides, `sp`→`dp` for text).
- Custom gesture-only interactions without an accessible alternative action
  (`Modifier.semantics { customActions = listOf(...) }`).

## 4. RTL / Arabic
- Use `start`/`end` padding, never `left`/`right`.
- Mirror directional icons: `Modifier.graphicsLayer { scaleX = if (isRtl) -1f else 1f }` or use
  `automirrored` icons (`Icons.AutoMirrored.Filled.ArrowBack`).
- Test with `LocalLayoutDirection provides LayoutDirection.Rtl` and `@Preview(locale = "ar")`.
- Numbers: use `NumberFormat.getInstance(locale)` — do not concatenate digits manually.
- Keep `android:supportsRtl="true"` in the manifest.

## 5. Typography and text
```kotlin
Text(
    text = title,
    style = MaterialTheme.typography.titleMedium,
    maxLines = 2,
    overflow = TextOverflow.Ellipsis,   // never clip silently
)
```
- Line length 45–75 characters for body text.
- Do not lock `maxLines = 1` on user-generated or translated strings without ellipsis.
- Use `sp` for text, `dp` for everything else.

## 6. Testing
```kotlin
composeTestRule.onNodeWithContentDescription("Add to favorites").assertHasClickAction()
composeTestRule.onRoot().printToLog("A11Y")     // dump the semantics tree
```
- Manual: TalkBack sweep of every screen, Switch Access, 200% font, dark mode.
- Automated: Accessibility Scanner (Play Store app) + `AccessibilityChecks.enable()` in Espresso.
- Add a CI screenshot test at `fontScale = 2f` to catch clipped layouts.

## 7. Checklist
- [ ] TalkBack reads every screen in a logical order with meaningful labels.
- [ ] All targets ≥ 48dp; focus ring visible with 3:1 contrast.
- [ ] Contrast tokens verified against the palette, both themes.
- [ ] Layout intact at 200% font scale and in Arabic RTL.
- [ ] No meaning conveyed by color alone.
- [ ] Accessibility Scanner reports zero critical issues.

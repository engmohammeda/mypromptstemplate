# One token set, every platform — reference

## 1. Source of truth
Keep tokens in a platform-neutral JSON (Design Tokens Community Group format) and generate
platform code with Style Dictionary. Never hand-maintain the same value in four languages.

```
tokens/
├── color.json
├── size.json
├── typography.json
└── motion.json
```

```bash
style-dictionary build --config sd.config.js
# → compose/Tokens.kt, flutter/tokens.dart, web/tokens.css, ios/Tokens.swift
```

## 2. Mapping table

| Concept | Compose (Android) | Flutter | SwiftUI | Web / Tailwind |
|---|---|---|---|---|
| Theme root | `MaterialTheme` + `CompositionLocal` | `ThemeData` / `InheritedWidget` | `Environment` values | CSS custom properties on `:root` |
| Color role | `ColorScheme.primary` | `ColorScheme.primary` | `Color("Primary")` asset | `--color-primary` / `bg-primary` |
| Dark theme | `isSystemInDarkTheme()` | `ThemeMode.system` | `@Environment(\.colorScheme)` | `prefers-color-scheme` / `dark:` |
| Spacing | `Dp` in a `Spacing` data class | `EdgeInsets` constants | `CGFloat` constants | `--space-m` / `p-4` |
| Type | `Typography` / `TextStyle` | `TextTheme` | `Font` + `.textStyle` | `--font-body-l` / `text-base` |
| Shape | `Shapes` / `RoundedCornerShape` | `ShapeThemeData` | `.clipShape` | `--radius-m` / `rounded-xl` |
| Elevation | `tonalElevation` / `shadowElevation` | `Material(elevation:)` | `.shadow` | `--shadow-2` |
| Motion | `tween`/`spring` + tokens | `Curves` + `Duration` | `.animation(.spring)` | `--duration-medium`, `--ease-standard` |
| Density unit | `dp` / `sp` | logical pixels / `sp`-like | points | `rem` (never `px` for text) |
| RTL | `LocalLayoutDirection` | `Directionality` | `.environment(\.layoutDirection)` | `dir="rtl"` + logical properties |

## 3. Platform conventions you must respect (do not "unify" these)

| Aspect | Android | iOS | Web |
|---|---|---|---|
| Back | System back / predictive back | Swipe from edge + top-left chevron | Browser back |
| Navigation | Bottom bar / rail / drawer | Tab bar / navigation stack | Header nav / sidebar |
| Primary action | FAB or bottom button | Top-right bar button or bottom button | Top-right or inline |
| Sheets | Bottom sheets | Sheets / action sheets | Modals / drawers |
| Typography | Roboto / dynamic | SF Pro / Dynamic Type | System stack |
| Switch vs checkbox | Switch = immediate effect | same | same |
| Alerts | Material dialog | UIAlertController style | Modal dialog |

Cross-platform apps should share **tokens and content**, not chrome. A Cupertino-looking Android
app feels foreign, and vice versa.

## 4. Web specifics
```css
:root {
  --color-surface: #fdfcff;
  --space-m: 1rem;
  --radius-m: 0.75rem;
  --duration-medium: 300ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}
@media (prefers-color-scheme: dark) { :root { --color-surface: #0f1214; } }
@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }
```
- Use **logical properties** (`margin-inline-start`, `padding-block`) so RTL works for free.
- `rem` for text, never `px`; respect the user's browser font size.
- Focus visible: never `outline: none` without an equally visible replacement.

## 5. Flutter specifics
```dart
final theme = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1B6EF3)),
  textTheme: appTextTheme,
  extensions: const [AppSpacing(m: 16, l: 24)],
);
```
Use `ThemeExtension` for tokens Material doesn't cover; never hardcode in widgets.

## 6. Consistency enforcement
- Lint rule / detekt rule banning raw `Color(0x`, `\.dp` literals and `\.sp` literals in feature modules.
- Stylelint `declaration-property-value-allowed-list` for web.
- A CI job that regenerates tokens and fails if the generated files differ from the committed ones
  (guarantees nobody hand-edited the output).
- Screenshot tests as the last line of defence.

## 7. Handoff checklist to engineers
- [ ] Token JSON committed + generated outputs per platform.
- [ ] Component spec per component: anatomy, sizes, all states, spacing, motion, a11y notes.
- [ ] Redlines only where behaviour is non-obvious (spacing comes from tokens, not from measurement).
- [ ] Light/dark/RTL/large-font examples for each component.
- [ ] Do/Don't examples for the tricky components.
- [ ] A single named owner for the system and a change-request process.

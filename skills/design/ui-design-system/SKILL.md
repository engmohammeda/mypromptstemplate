---
name: ui-design-system
description: >-
  Designs and enforces a visual design system: design tokens, color and theming (light/dark,
  Material 3 dynamic color), typographic scale, 4/8pt spacing grid, elevation, shape, iconography,
  motion and component specs, implemented as code for Compose, Flutter, or web. Use when the user
  mentions design system, design tokens, theme, color palette, typography, spacing, styleguide,
  Material 3, dark mode, brand colors, component library, visual consistency, or asks how a screen
  should look or why a UI looks unprofessional.
version: 1.0.0
license: MIT
category: design
tags: [design-system, tokens, material3, color, typography, spacing, theming]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "بناء نظام تصميم كامل: توكنز، ألوان وثيمات، سلم طباعة، شبكة مسافات، وحركة — كود لا صور."
---

# UI Design System

You are the design-systems lead. **Nothing in the UI is arbitrary**: every color, size and duration
comes from a named token with a documented reason.

## When to use
- Starting a product's visual language, or fixing an inconsistent one.
- Deciding colors, type scale, spacing, radii, elevation, motion.
- Reviewing a UI that "looks off" but nobody can say why.

## When NOT to use
- Flows, information architecture, usability → `ux-flow-architect`.
- Compose implementation mechanics → `android-compose-ui`.
- Logo/brand identity creation → `logo-brand-designer`.

## Non-negotiables
- **MUST** define tokens in **three tiers**: *primitive* (`blue-500`) → *semantic* (`color.surface.container`) → *component* (`button.primary.background`). Components reference semantic tokens only.
- **MUST** use a spacing scale of 4dp steps (4, 8, 12, 16, 24, 32, 48, 64). **NEVER** an arbitrary `13.dp`.
- **MUST** define a type scale with a fixed ratio (1.200 minor third or 1.250 major third), max 7 steps, each with size/line-height/weight/tracking.
- **MUST** meet contrast: 4.5:1 body text, 3:1 large text and non-text UI (borders, icons, focus rings) — in **both** themes.
- **MUST** design light and dark as **first-class pairs**; dark is not "invert the colors". Use elevated surface tints, never pure `#000` backgrounds for large areas, and desaturate accents in dark.
- **MUST** limit the palette: 1 primary, 1 secondary/accent, 1 neutral ramp (9–11 steps), plus semantic success/warning/error/info.
- **MUST** define motion tokens (duration + easing) and honour "reduce motion".
- **NEVER** hardcode a color, radius, font size or duration in feature code — only in the token layer.
- **NEVER** use more than 2 typefaces (ideally 1 family with weights).
- **NEVER** rely on color alone to convey state.

## Version pins
| Item | Value |
|---|---|
| Material Design | M3 (Expressive guidelines) |
| WCAG | 2.2 level AA |
| Compose Material 3 | via Compose BOM 2026.08.00 |
| Token tooling | Style Dictionary 4.x (optional, for multi-platform export) |

## Workflow
1. **Audit or brief**: collect the brand inputs (logo, brand colors, tone) and the platforms to support.
2. **Neutral ramp first** — build the greys; 80% of a professional UI is neutrals used correctly.
3. **Pick the primary** and generate a tonal palette (M3 tonal values 0–100); derive the semantic roles.
4. **Verify contrast** for every foreground/background pair in both themes; adjust tones, not opacity.
5. **Define the type scale** (display/headline/title/body/label), line-height 1.4–1.6 for body, tracking rules.
6. **Define spacing, radius, elevation, border** tokens.
7. **Define motion**: durations (short 100–200ms, medium 250–400ms, long 450–600ms) and easing (emphasized/standard).
8. **Write the theme in code** (`core:designsystem`) and expose it via `MaterialTheme` + a custom `LocalAppTokens`.
9. **Build the component library**: button, text field, card, chip, dialog, snackbar, list item, empty state, loading, error — each with all states (enabled/hover/pressed/focused/disabled/error/loading).
10. **Document + screenshot-test** every component in light/dark/RTL/large-font.

## Patterns

✅ **Token tiers in Compose**
```kotlin
// Tier 1 — primitives (never used directly by features)
internal object Palette {
    val Blue40 = Color(0xFF1B6EF3); val Blue80 = Color(0xFFAFC6FF)
    val Neutral10 = Color(0xFF1A1C1E); val Neutral99 = Color(0xFFFDFCFF)
}

// Tier 2 — semantic, theme-aware
private val LightColors = lightColorScheme(
    primary = Palette.Blue40, onPrimary = Color.White,
    surface = Palette.Neutral99, onSurface = Palette.Neutral10,
)
private val DarkColors = darkColorScheme(
    primary = Palette.Blue80, onPrimary = Color(0xFF002E6A),
    surface = Palette.Neutral10, onSurface = Color(0xFFE2E2E6),
)

@Immutable
data class Spacing(
    val xs: Dp = 4.dp, val s: Dp = 8.dp, val m: Dp = 16.dp,
    val l: Dp = 24.dp, val xl: Dp = 32.dp, val xxl: Dp = 48.dp,
)
val LocalSpacing = staticCompositionLocalOf { Spacing() }

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colors = when {
        dynamicColor && Build.VERSION.SDK_INT >= 31 ->
            if (darkTheme) dynamicDarkColorScheme(LocalContext.current)
            else dynamicLightColorScheme(LocalContext.current)
        darkTheme -> DarkColors
        else -> LightColors
    }
    CompositionLocalProvider(LocalSpacing provides Spacing()) {
        MaterialTheme(colorScheme = colors, typography = AppTypography, shapes = AppShapes, content = content)
    }
}
```

✅ **Type scale (1.250 ratio, 16sp base)**
```kotlin
val AppTypography = Typography(
    displaySmall = TextStyle(fontSize = 36.sp, lineHeight = 44.sp, fontWeight = FontWeight.SemiBold),
    headlineSmall = TextStyle(fontSize = 24.sp, lineHeight = 32.sp, fontWeight = FontWeight.SemiBold),
    titleMedium = TextStyle(fontSize = 20.sp, lineHeight = 28.sp, fontWeight = FontWeight.Medium),
    bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp),   // 1.5 line-height
    bodyMedium = TextStyle(fontSize = 14.sp, lineHeight = 20.sp),
    labelLarge = TextStyle(fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium, letterSpacing = 0.1.sp),
)
```

❌ **Don't**
```kotlin
Text("Title", fontSize = 17.sp, color = Color(0xFF3A3A3A))  // off-scale, off-palette
Card(shape = RoundedCornerShape(7.dp), elevation = 3.dp)     // arbitrary values
Box(Modifier.padding(start = 13.dp, top = 11.dp))            // breaks the grid
```

## Anti-patterns
- A "design system" that is a Figma file with no code counterpart — it will drift within a month.
- 40 shades of grey because each screen picked its own.
- Dark theme built by inverting: pure black surfaces, full-saturation accents, invisible dividers.
- Elevation used decoratively rather than to express hierarchy.
- Component variants created ad hoc per screen (`PrimaryButtonBigRed`).
- Font sizes in `dp`, blocking user font scaling.
- Motion durations of 600ms+ on frequent interactions (feels sluggish).
- Overriding `MaterialTheme` values locally "just for this screen".

## Definition of Done
- [ ] Three-tier tokens implemented in code; zero raw values in feature modules (lint-enforced).
- [ ] Light and dark palettes both pass WCAG AA for every text/background pair.
- [ ] Type scale ≤ 7 steps with defined line-heights; renders correctly at 200% font scale.
- [ ] Spacing strictly on the 4dp grid; radius/elevation tokenised.
- [ ] Motion tokens defined; reduced-motion honoured.
- [ ] Component library covers every state, documented with previews.
- [ ] Screenshot tests for all components: light, dark, RTL, fontScale 2.0.
- [ ] A `docs/design-system.md` explains *when* to use each token, not just what exists.

## References
- `references/design-laws.md` — the perceptual and cognitive laws behind these rules (Gestalt, Fitts, Hick, Miller, Von Restorff, Jakob).
- `references/color-and-typography.md` — building palettes, contrast math, tonal ramps, type pairing, Arabic type.
- `references/spacing-layout-motion.md` — grid, rhythm, density, elevation, motion curves and durations.
- `references/platform-mapping.md` — the same tokens expressed in Compose, Flutter, SwiftUI, CSS/Tailwind.
- Material 3: https://m3.material.io · WCAG 2.2: https://www.w3.org/TR/WCAG22/

## ملخص عربي
نظام التصميم كود لا صور. التوكنز على ثلاث طبقات: أولية ← دلالية ← مكوّن، والميزات تستخدم الطبقة
الدلالية فقط. شبكة مسافات من مضاعفات ٤، وسلم طباعة بنسبة ثابتة لا يتجاوز ٧ درجات، وتباين لا يقل
عن 4.5:1 للنص في الوضعين الفاتح والداكن. الوضع الداكن يُصمَّم لا يُعكس. مكتبة مكوّنات تغطي كل
الحالات مع اختبارات لقطات شاشة في الفاتح والداكن وRTL وتكبير الخط.

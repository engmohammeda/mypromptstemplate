# Color & typography — reference

## 1. Building the palette

### Step 1 — the neutral ramp (do this first)
Generate 11 steps from near-white to near-black, with a slight hue tint (2–6% of your brand hue)
so greys feel intentional rather than dead.

| Token | Light theme use | Dark theme use |
|---|---|---|
| N-0 `#FFFFFF` | page background | — |
| N-50 | subtle surface | — |
| N-100 | card / container | — |
| N-200 | borders, dividers | — |
| N-400 | disabled text/icons | disabled |
| N-600 | secondary text | secondary text |
| N-800 | primary text | — |
| N-900 | headings | surface (elevated) |
| N-950 `#0F1214` | — | page background |

Dark surfaces: never `#000000` for large areas (OLED smearing, harsh contrast). Use `#0F1214`–`#121417`
and express elevation with lighter surface tints (+4%, +8%, +12% lightness), not shadows.

### Step 2 — the primary tonal palette
Take the brand hue and generate tones 0–100 (M3 style). Then map roles:

| Role | Light | Dark |
|---|---|---|
| `primary` | tone 40 | tone 80 |
| `onPrimary` | tone 100 | tone 20 |
| `primaryContainer` | tone 90 | tone 30 |
| `onPrimaryContainer` | tone 10 | tone 90 |

This mapping is why M3 themes are automatically contrast-safe. Do not invent your own mapping
without checking every pair.

### Step 3 — semantic status colors
`success` (green 600/300), `warning` (amber 700/300), `error` (red 600/300), `info` (blue 600/300),
each with a container variant. Always pair with an icon and text — never color alone.

## 2. Contrast math

Relative luminance `L = 0.2126R + 0.7152G + 0.0722B` (linearised channels).
Ratio = `(L_lighter + 0.05) / (L_darker + 0.05)`.

| Content | Minimum (AA) | Enhanced (AAA) |
|---|---|---|
| Body text (< 18.66px bold / 24px) | 4.5:1 | 7:1 |
| Large text | 3:1 | 4.5:1 |
| Icons, borders, focus rings, chart strokes | 3:1 | — |
| Disabled elements | exempt, but keep ≥ 2:1 for usability |

Practical rules:
- Placeholder text at 3:1 is a WCAG failure if it conveys information — use a persistent label.
- Do not fix contrast with opacity on a colored surface; pick a different tone.
- Test on a real device at minimum brightness in daylight — the lab is not the world.

Tools: `python -c` with the formula above, Material Theme Builder, or a CI check that iterates all
token pairs and fails the build on a violation.

## 3. Dynamic color (Android 12+)
- `dynamicLightColorScheme` / `dynamicDarkColorScheme` derive from the user's wallpaper — respect it
  unless brand color is functionally essential (e.g. a bank's identity).
- Always keep the static brand scheme as the fallback and test both.
- Brand-critical elements (the logo, a status color) must **not** be dynamic.

## 4. Typography

### Choosing typefaces
- One family, 3–4 weights (Regular 400, Medium 500, SemiBold 600, Bold 700 only if needed).
- System fonts (Roboto/SF/Inter) are safe, fast, and already hinted for screens.
- A display face for headings is allowed only if it has a real brand purpose — never for body text.
- Check the licence for commercial use and for embedding in an app.

### The scale (ratio 1.250, base 16)
| Step | Size | Line height | Weight | Use |
|---|---|---|---|---|
| Display | 36–45 | 1.15 | 600 | hero, rare |
| Headline | 28–32 | 1.25 | 600 | screen title |
| Title | 20–22 | 1.3 | 500 | section, dialog title |
| Body L | 16 | 1.5 | 400 | primary content |
| Body M | 14 | 1.45 | 400 | secondary |
| Label | 14 | 1.4 | 500 | buttons, chips |
| Caption | 12 | 1.4 | 400 | metadata (never for essential text) |

Rules:
- Line-height 1.4–1.6 for body; 1.1–1.25 for large headings.
- Letter-spacing: slightly negative (−0.5 to −1%) for large headings, 0 for body, +0.5 to +1% for
  all-caps labels. Never letter-space Arabic.
- Never centre paragraphs of more than 2 lines.
- Truncate with an ellipsis and provide the full text elsewhere; never clip silently.
- Text sizes in `sp`/scalable units so system font scaling works.

## 5. Arabic & RTL typography
- Arabic needs **more vertical space**: increase line-height by ~10–15% vs. Latin (1.6–1.75 for body).
- Do **not** apply letter-spacing or fake-bold to Arabic — it breaks letter joining.
- Choose a font with proper Arabic support: Noto Naskh Arabic / Noto Sans Arabic, IBM Plex Sans Arabic,
  Cairo, Tajawal. Verify the Latin and Arabic faces have compatible x-heights and weights.
- Arabic glyphs are optically smaller at the same point size; bump Arabic body by 1–2sp.
- Numerals: decide Western (0-9) vs. Arabic-Indic (٠-٩) per locale and apply consistently via
  `NumberFormat`; do not mix within a screen.
- Mirror the layout, not the content: logos, charts with a time axis, and media playback controls
  follow specific rules — see `android-compose-ui/references/compose-accessibility.md`.
- Test every screen with a real Arabic translation, not lorem ipsum — length differs by ±30%.

## 6. Deliverable format
Export tokens once, consume everywhere (Style Dictionary):
```json
{
  "color": { "brand": { "primary": { "value": "#1B6EF3" } } },
  "space": { "m": { "value": "16", "type": "dimension" } },
  "font": { "body-l": { "value": { "size": "16", "lineHeight": "24", "weight": "400" } } }
}
```
Build targets: Compose `Color`/`Dp` objects, Flutter `ThemeData`, CSS custom properties,
Tailwind config, iOS `UIColor`. One source of truth, zero drift.

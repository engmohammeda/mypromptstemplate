---
name: app-icon-designer
description: >-
  Designs and produces app icons and in-app iconography: Android adaptive, themed (monochrome) and
  Play Store icons, iOS app icons, favicons and PWA icons, plus a consistent UI icon set with correct
  grids, keylines, optical balance and export pipelines. Use when the user mentions app icon,
  launcher icon, adaptive icon, monochrome icon, ic_launcher, mipmap, favicon, PWA icon, icon set,
  vector drawable, SVG icons, icon sizes, or asks to design or export icons for any platform.
version: 1.0.0
license: MIT
category: design
tags: [icons, adaptive-icon, android, ios, favicon, svg, vector, assets]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "تصميم وإنتاج أيقونة التطبيق (تكيفية/أحادية/متجر) ومجموعة أيقونات الواجهة بكل المقاسات."
---

# App Icon Designer

You are the icon designer. An icon is a **20×20-pixel-legible symbol**, not a shrunken illustration.

## When to use
- Creating or refreshing an app launcher icon for any platform.
- Building a consistent in-app icon set.
- Generating and wiring every required size/format.

## When NOT to use
- Full brand identity, wordmark, brand guidelines → `logo-brand-designer`.
- Store screenshots and feature graphic → `android-play-release`.

## Non-negotiables
- **MUST** design on the platform grid with the correct **safe zone**: Android adaptive icons are 108×108dp with only the **central 66dp** guaranteed visible (72dp diameter mask varies by OEM).
- **MUST** ship **three** Android variants: full-color adaptive (foreground + background layers), **monochrome** layer for themed icons, and the 512×512 Play Store icon.
- **MUST** verify legibility at **48dp, 24dp and 16dp** before approving anything.
- **MUST** use vectors as the source (`SVG` → `VectorDrawable`); raster only where the platform demands it.
- **NEVER** put text or a wordmark inside an app icon (illegible and unlocalisable).
- **NEVER** bake a shadow, a rounded-rect frame, or a mask into the Android adaptive foreground — the system applies the mask and elevation.
- **NEVER** include an alpha channel in the 512×512 Play Store icon.
- **NEVER** mix icon styles in one UI set (filled + outlined + duotone at random).
- **MUST** keep in-app icons on a 24×24dp grid with a 2dp stroke and 1–2dp padding, optically balanced rather than mathematically centred.

## Version pins / specs
| Asset | Spec |
|---|---|
| Android adaptive foreground/background | 108×108dp; safe zone: central 66dp; export 432×432px @4x |
| Android monochrome (themed icons) | same geometry, single color, alpha defines the shape |
| Play Store icon | 512×512 PNG, 32-bit, **no alpha**, ≤ 1 MB |
| Legacy `mipmap` PNGs | 48/72/96/144/192 px (mdpi→xxxhdpi) — only for API < 26 support |
| iOS app icon | 1024×1024 PNG, no alpha, no rounded corners (system masks) |
| Favicon | `favicon.svg` + `favicon.ico` (16/32/48) + `apple-touch-icon.png` 180×180 |
| PWA | 192×192, 512×512, plus a 512×512 `maskable` with a 20% safe padding |
| UI icon grid | 24×24dp canvas, 20×20 live area, 2dp stroke, 2dp corner radius |

## Workflow
1. **Extract the concept**: one idea, from the brand's core metaphor. Not the whole logo shrunk.
2. **Sketch at 48dp first** — if it doesn't read there, it never will.
3. **Build on the grid** with keylines (circle Ø 64, square 60×60, rectangles 60×44 / 44×60) for optical consistency.
4. **Design the layers**: background (a flat color/gradient that fills 108×108), foreground (the symbol within the 66dp safe zone), monochrome (silhouette that still reads in one color).
5. **Test the masks**: circle, squircle, rounded square, teardrop, and the parallax/animation crop.
6. **Test in context**: on a light wallpaper, a dark wallpaper, a busy photo, next to Gmail/WhatsApp, in the notification bar (monochrome, 24dp), and in the Play listing grid.
7. **Export the full matrix** with a script (see `references/export-pipeline.md`); never hand-resize.
8. **Wire it up**: `mipmap-anydpi-v26/ic_launcher.xml`, round variant, monochrome, and the manifest reference.
9. **Verify on device** across launchers (Pixel, One UI, MIUI) and in themed-icon mode.

## Patterns

✅ **Adaptive icon XML (`res/mipmap-anydpi-v26/ic_launcher.xml`)**
```xml
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />
</adaptive-icon>
```
Manifest:
```xml
<application
    android:icon="@mipmap/ic_launcher"
    android:roundIcon="@mipmap/ic_launcher_round" />
```

✅ **UI icon as a VectorDrawable (24dp grid, 2dp stroke)**
```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24"
    android:tint="?attr/colorControlNormal"
    android:autoMirrored="true">
    <path android:fillColor="@android:color/white"
        android:pathData="M12,4 L4,12 h3 v6 h10 v-6 h3 Z" />
</vector>
```
`autoMirrored="true"` for directional icons so RTL works automatically.

❌ **Don't**
```
- A 512px illustration with 6 colors, gradients and a tagline, downscaled to 48dp
- Foreground artwork touching the 108dp edges → cropped on circular masks
- A drop shadow drawn into the foreground layer → doubled shadow on Pixel launchers
- Icon set mixing 1.5dp and 2dp strokes, or filled and outlined styles
- PNG-only icons in `drawable/` instead of vectors
```

## Anti-patterns
- Designing at 1024px and never checking 24px.
- Photographic or gradient-heavy icons — they turn to mud at small sizes.
- Depending on color to distinguish two icons in the same set.
- Skipping the monochrome layer → your icon looks broken in Android themed-icon mode.
- Using stock icons from mixed sets (different grids, weights and metaphors).
- Non-optical centring: a triangle mathematically centred always looks off — nudge it.
- Alpha channel in the store icon → Play rejects the upload.
- Different icons per density that are not pixel-consistent.

## Definition of Done
- [ ] Concept is one clear metaphor, legible at 16/24/48dp.
- [ ] Adaptive foreground respects the 66dp safe zone; background fills the full 108dp.
- [ ] Monochrome layer provided and tested in themed-icon mode.
- [ ] 512×512 store icon, no alpha, matches the in-app icon.
- [ ] All masks (circle, squircle, rounded square, teardrop) verified — nothing clipped.
- [ ] Tested on light/dark wallpapers and beside popular apps.
- [ ] iOS 1024 / favicon set / PWA maskable exported if those platforms are targeted.
- [ ] UI icon set: one grid, one stroke weight, one style; directional icons auto-mirrored.
- [ ] All assets generated by a repeatable script, committed with the source SVGs.

## References
- `references/icon-specs.md` — every size and format table per platform, plus grid/keyline rules.
- `references/export-pipeline.md` — scripts for generating the full asset matrix and validating it.
- Adaptive icons: https://developer.android.com/develop/ui/views/launch/icon_design_adaptive
- Material icon guidelines: https://m3.material.io/styles/icons

## ملخص عربي
الأيقونة رمز واحد واضح عند ٢٤ بكسل لا رسمة مصغّرة. على أندرويد صمّم أيقونة تكيفية بطبقتين ضمن
منطقة آمنة قطرها 66dp من أصل 108dp، مع طبقة أحادية اللون إلزامية للأيقونات المتناسقة مع الثيم،
وأيقونة متجر 512×512 بلا قناة شفافية. ممنوع النص أو الظل أو الإطار داخل الأيقونة. أيقونات الواجهة
على شبكة 24 وبسماكة خط موحّدة وأسلوب واحد، وتُصدَّر كلها بسكربت لا يدويًا.

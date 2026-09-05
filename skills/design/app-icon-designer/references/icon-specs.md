# Icon specifications — reference

## 1. Android launcher icon

### Adaptive icon geometry
```
108 × 108 dp total canvas
 ├─ 72 dp  visible mask area (varies by OEM shape)
 └─ 66 dp  guaranteed safe zone (centre) ← keep ALL meaningful artwork here
```
- The outer 18dp on each side is used for parallax and mask cropping — expect it to be cut.
- Background layer: must fill the entire 108×108 (no transparency at the edges).
- Foreground layer: transparent outside the symbol; no shadows, no mask, no frame.
- Export each layer as a VectorDrawable if possible; otherwise 432×432 px PNG (4×).

### Required files
```
res/mipmap-anydpi-v26/ic_launcher.xml
res/mipmap-anydpi-v26/ic_launcher_round.xml
res/drawable/ic_launcher_foreground.xml     (vector)
res/drawable/ic_launcher_background.xml     (vector or color)
res/drawable/ic_launcher_monochrome.xml     (vector, single path, alpha shape)
res/mipmap-{m,h,xh,xxh,xxxh}dpi/ic_launcher.png        48/72/96/144/192 px  (API < 26)
res/mipmap-{m,h,xh,xxh,xxxh}dpi/ic_launcher_round.png  same sizes
play/icon-512.png                                       512×512, no alpha
```

### Monochrome layer rules
- Single color; the **alpha channel defines the shape**, the color is applied by the system.
- Simplify: remove inner detail that disappears when everything is one tone.
- The silhouette must still be recognisable — test by flattening your foreground to black.
- Same 66dp safe zone.

### Notification icon (separate asset!)
- 24×24dp, **white on transparent only** — any color is stripped to a white silhouette.
- Put it in `res/drawable/ic_notification.xml`.
- Using the launcher icon here produces a grey blob. This is the most common Android icon bug.

## 2. iOS
| Asset | Size |
|---|---|
| App Store / app icon (single size, Xcode generates the rest) | 1024×1024 PNG, no alpha, square, no rounded corners |
| Optional dark & tinted variants (iOS 18+) | 1024×1024 each |

Design on the iOS grid (rounded superellipse mask, ~22.37% corner radius) but never draw the mask.

## 3. Web
| Asset | Size / notes |
|---|---|
| `favicon.svg` | vector, with `prefers-color-scheme` handling if needed |
| `favicon.ico` | multi-size 16/32/48 |
| `apple-touch-icon.png` | 180×180, no transparency, no rounded corners |
| PWA `icon-192.png`, `icon-512.png` | manifest icons |
| PWA maskable | 512×512 with the symbol inside the central 80% (safe zone), `"purpose": "maskable"` |

```json
{
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

## 4. Other targets
| Platform | Spec |
|---|---|
| Wear OS | Same adaptive icon; verify on the circular mask |
| Android TV | Banner 320×180 px, xhdpi, with the app name baked in |
| Windows / MSIX | 44×44, 150×150, 310×150, 310×310 + a scaled set (100/125/150/200/400%) |
| macOS | 1024×1024 with the macOS-specific inset (~10% padding) |
| Notification / status | 24dp white-on-transparent |
| Shortcut icons | 48dp adaptive, same safe-zone rules |

## 5. UI icon set rules

### Grid
```
24 × 24 dp canvas
 └─ 20 × 20 live area  (2dp padding all around)
Keylines: circle Ø 20 · square 18×18 · vertical rect 16×20 · horizontal rect 20×16
```

### Style contract (pick one and never mix)
| Property | Value |
|---|---|
| Style | outlined **or** filled **or** rounded — one per product |
| Stroke | 2dp uniform (1.5dp only for dense desktop UIs) |
| Terminals | butt or round — consistent |
| Corner radius | 2dp exterior, 1dp interior |
| Angles | 45° increments; avoid arbitrary angles |
| Detail | max 2 levels of detail; nothing thinner than 1dp |
| Color | inherit from theme (`tint`), never hardcoded |

### Optical rules
- A circle must be ~2% larger than a square to look the same size.
- Triangles and arrows need a nudge toward their visual centre of mass.
- Align to the pixel grid at 24dp to avoid blurry strokes.
- Keep the same visual weight across the set: squint at the whole sheet — no icon should pop.

### Naming convention
```
ic_<category>_<name>_<style>.xml
ic_action_save_outlined.xml
ic_nav_home_filled.xml
ic_status_error_filled.xml
```

## 6. Directional icons and RTL
Set `android:autoMirrored="true"` for: back/forward arrows, next/previous, send, reply, redo/undo,
list indentation, chevrons in list items, progress direction.
Do **not** mirror: play/pause (media transport is universal), clocks, checkmarks, logos, numbers.

## 7. Accessibility
- Icon-only buttons need a `contentDescription` and a 48dp touch target.
- Never rely on an icon alone for a critical action — pair with a label where space allows.
- Status icons need a 3:1 contrast against their background.
- Do not use color alone to differentiate two icons in the same set.

# Brand guidelines — fill-in template

> Deliver as `brand/guidelines.md` (and export to PDF). Every rule needs a visual example.

---

# <Brand> Brand Guidelines
Version 1.0 · <date> · Owner: <name/team> · Questions: <email>

## 1. Brand foundation

**Positioning**
> For <audience> who <need>, <Brand> is a <category> that <benefit>, unlike <alternative>,
> because <reason to believe>.

**Mission** — <one sentence>
**Personality** — <adjective>, <adjective>, <adjective>
**What we are not** — <3 anti-attributes, e.g. "not corporate, not childish, not loud">

## 2. Logo

### 2.1 Primary logo
<image> — Use this in ~80% of cases.

### 2.2 Variants and when to use each
| Variant | File | Use |
|---|---|---|
| Horizontal | `logo/svg/primary-color.svg` | Headers, documents, wide spaces |
| Stacked | `logo/svg/stacked-color.svg` | Square/narrow placements |
| Mark only | `logo/svg/mark-color.svg` | App icon, favicon, avatars, ≤ 64px |
| Wordmark | `logo/svg/wordmark-color.svg` | When the mark already appears nearby |
| Black | `...-black.svg` | Single-color print, engraving |
| White (knockout) | `...-white.svg` | Dark or photographic backgrounds |

### 2.3 Clear space
Minimum clear space on all sides = **x**, where x = <definition, e.g. the height of the 'o'>.
<diagram>

### 2.4 Minimum sizes
| Variant | Screen | Print |
|---|---|---|
| Horizontal | 120 px wide | 25 mm |
| Stacked | 80 px wide | 18 mm |
| Mark | 24 px | 6 mm |

### 2.5 Incorrect usage (each with a visual ❌)
- Do not stretch, squash or rotate.
- Do not change the colors or apply gradients.
- Do not add shadows, outlines, bevels or glows.
- Do not place on a background with < 3:1 contrast; use the knockout variant.
- Do not rearrange, resize or separate the lockup elements.
- Do not re-type the wordmark in another font.
- Do not enclose it in a shape that is not part of the system.
- Do not use the old logo (see `archive/`).

## 3. Color

| Role | Name | HEX | RGB | CMYK | Pantone |
|---|---|---|---|---|---|
| Primary | <name> | #______ | | | |
| Accent | | | | | |
| Ink (text) | | | | | |
| Surface | | | | | |
| Success / Warning / Error | | | | | |

Rules:
- Primary is for the brand and the single most important action — not for large fills.
- Minimum contrast 4.5:1 for text, 3:1 for UI elements.
- Full UI color ramps live in the design system (`core:designsystem`), derived from these.

## 4. Typography

| Role | Typeface | Weights | Fallback |
|---|---|---|---|
| Brand / display | <name> | 600 | <system> |
| UI / body | <name> | 400, 500, 600 | <system> |
| Arabic | <name, e.g. IBM Plex Sans Arabic> | 400, 500, 700 | Noto Sans Arabic |
| Mono (code/data) | <name> | 400 | monospace |

Licences: <where they are, what they permit>.
Scale, line-heights and usage rules: see the design system.

## 5. Imagery & illustration
- Photography: <style, subjects, treatment, what to avoid>.
- Illustration: <style, stroke, palette, when to use>.
- Iconography: see `app-icon-designer` — 24dp grid, <outlined/filled>, 2dp stroke.
- Never: stock photos of handshakes/generic offices, mismatched illustration styles, low-res assets.

## 6. Voice & tone
| Situation | Tone | Example |
|---|---|---|
| Onboarding | Warm, encouraging | "Let's set up your first project." |
| Error | Plain, accountable | "We couldn't save that. Check your connection and try again." |
| Success | Brief, specific | "Invite sent to sara@example.com" |
| Legal/payment | Precise, neutral | "You'll be charged $9 on 1 March." |

We say: <words we use>. We avoid: <jargon, hype words, "simply", "just">.

## 7. Applications
- App icon: <link to the icon spec>
- Social avatars and covers: `templates/`
- Presentation and document templates: `templates/`
- Merchandise / print: minimum sizes, single-color usage, embroidery notes.
- Email signature, favicon, watermark.

## 8. Bilingual / Arabic system
- Arabic logotype: `logo/svg/primary-ar-*.svg` — see `arabic-bilingual-branding.md`.
- Lockup order in RTL contexts, spacing, and which variant is primary in each market.

## 9. Asset access & governance
- Assets: `brand/` in this repository (single source of truth).
- Requests for a new variant or an exception: <process, owner>.
- Changelog:
  | Version | Date | Change |
  |---|---|---|
  | 1.0 | | Initial release |

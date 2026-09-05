# Logo construction — reference

## 1. Concept before form

Write 3–5 concepts as sentences. If you cannot say it, you cannot draw it.
```
Concept A — "Compounding": overlapping arcs that build a larger form, for a savings product.
Concept B — "The checkpoint": a mark derived from a check + a location pin, for a delivery app.
Concept C — "Monogram T with motion": the letter T with a swept counter, suggesting speed.
```
Reject any concept that is: a category cliché, a hidden pun nobody sees in 1 second, or
impossible to render at 24px.

## 2. Types of marks

| Type | Best when | Risk |
|---|---|---|
| Wordmark (logotype) | Distinctive name, needs recognition-building | Long names fail at small sizes |
| Lettermark / monogram | Long or generic names | Crowded space; easy to look like an existing mark |
| Pictorial mark | Concrete, ownable object | Can be literal/limiting |
| Abstract mark | Broad or evolving business | Needs budget to build meaning |
| Combination (mark + word) | Most products — flexible | Requires disciplined lockups |
| Emblem | Heritage, badges | Poor at small sizes and in horizontal spaces |

For an app, you almost always need a **combination mark** with a strong standalone symbol,
because the app icon has no room for the wordmark.

## 3. Geometric construction
- Build from primitives: circles, squares, arcs at 45°/90° increments; keep relationships rational (1:1, 1:2, 1:1.5, φ where it genuinely helps).
- Consistent stroke weight across the mark; if you taper, taper systematically.
- Corner radii from one scale; do not mix sharp and rounded arbitrarily.
- Counters (enclosed negative spaces) must survive at small sizes — widen them beyond what looks right at large size.
- Keep the total path count low; complexity is the enemy of scalability.

## 4. Optical corrections (mathematics lies to the eye)
- Circles must **overshoot** flat shapes by ~1.5–2% to appear the same size.
- Horizontal strokes appear heavier than vertical ones — thin them ~5–8%.
- The optical centre is ~5% above the mathematical centre. Place marks accordingly in a container.
- Pointed shapes (triangles, arrows) need extra overshoot at the apex.
- Letter spacing in a wordmark is kerned by eye, pair by pair — never rely on the font's defaults.
- Test by flipping the artwork horizontally; imbalance becomes obvious.

## 5. Typography for the wordmark
- Start from a licensed typeface, then **customise**: adjust terminals, kerning, one distinctive letterform.
- Avoid: Papyrus, Comic Sans, Bleeding Cowboys, over-familiar defaults, and any font whose licence
  forbids logo use (check the EULA — several popular foundries do restrict it).
- Convert text to outlines in delivered masters so no font is required downstream.
- Keep the wordmark to one weight; if you need two, there must be a hierarchy reason.
- Tracking: slightly looser for small sizes, tighter for large display use — hence separate
  "small use" variants for the best identities.

## 6. Stress test suite (all must pass)

| Test | Method | Pass criterion |
|---|---|---|
| Small size | Render at 16, 24, 32, 48px | Silhouette still identifiable |
| Squint / blur | Gaussian blur 8px | The overall shape is still distinct |
| Grayscale | Desaturate | Hierarchy intact, no elements merging |
| Inverted | White on black | No filled areas becoming illegible |
| One-color | Pure black fill only | Works without any tonal separation |
| Single-color print | Fax/stamp/engrave simulation | No hairlines below 0.25pt |
| Photo background | Place on 3 busy photos | Needs the knockout variant to work |
| Distance | View at 3m on a laptop screen | Recognisable |
| Competitor row | Place beside 8 competitors | Distinguishable at a glance |
| App icon | Crop into the 66dp safe zone | The mark alone carries the brand |
| Favicon | 16×16 | Not a mush |
| Rotation/flip | Mirror it | No accidental offensive/odd form |

```bash
# quick raster stress sheet
for s in 16 24 32 48 96 256; do rsvg-convert -h $s logo-mark.svg -o test-$s.png; done
magick logo-mark.svg -colorspace Gray test-gray.png
magick logo-mark.svg -blur 0x8 test-blur.png
magick logo-mark.svg -negate test-invert.png
```

## 7. Clear space & minimum size
Define clear space as a multiple of a measurable element of the logo itself (e.g. the height of the
"o", or the mark's stroke width × 4) so it scales automatically.

```
┌─────────────────────────────┐
│         ↕ x                 │
│   x ↔  [ LOGO ]  ↔ x        │
│         ↕ x                 │
└─────────────────────────────┘
x = height of the wordmark's lowercase 'o'
```
Minimum sizes: state them in **px for screen** and **mm for print**, per variant.

## 8. Color for brand
- Primary brand color + 1 accent maximum at identity level. UI needs more — that's the design system's job.
- Provide HEX/RGB (screen), CMYK (print), and Pantone (spot) values. Convert deliberately: an RGB
  brand color often needs a hand-tuned CMYK equivalent, not an automatic conversion.
- Check the color against cultural meanings in target markets (white = mourning in parts of Asia;
  green has religious connotations in parts of the Middle East; red = luck in China, danger in the West).
- Ensure the brand color can pass 4.5:1 against white **or** provide a darker "on-light" variant for text.

## 9. Legal & practical checks
- [ ] Trademark search in target jurisdictions (national IP office databases + a common-law search).
- [ ] Domain and social handle availability.
- [ ] Font licence permits logo use, embedding and commercial distribution.
- [ ] No stock asset with a licence forbidding trademark registration.
- [ ] Name pronounceable and non-offensive in the target languages.
- [ ] Reverse-image search the final mark for accidental similarity.

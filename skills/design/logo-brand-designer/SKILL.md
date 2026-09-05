---
name: logo-brand-designer
description: >-
  Creates and evaluates brand identity: logo concept and construction, logotype and monogram,
  clear space and minimum sizes, responsive logo variants, color and typography for brand, brand
  voice, and a usage guideline document with correct/incorrect examples. Use when the user mentions
  logo, brand, branding, brand identity, wordmark, monogram, logo variants, brand guidelines,
  style guide, brand colors, naming, visual identity, or asks to design or critique a logo.
version: 1.0.0
license: MIT
category: design
tags: [branding, logo, identity, brand-guidelines, wordmark, visual-identity]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "بناء هوية بصرية: مفهوم الشعار وبناؤه، المتغيرات، المساحة الآمنة، ودليل استخدام كامل."
---

# Logo & Brand Designer

You are the brand designer. A logo is not art — it is a **functional identification system** that
must survive a 16px favicon, an embroidered shirt, and a black-and-white fax.

## When to use
- Creating a new brand identity or refreshing one.
- Critiquing an existing logo objectively.
- Producing brand guidelines and the asset kit.

## When NOT to use
- App launcher icon production → `app-icon-designer` (the logo is an input to it).
- Product UI tokens → `ui-design-system` (brand colors feed it, but UI needs a full ramp).

## Non-negotiables
- **MUST** start from a positioning statement: who it's for, what it does, what makes it different, and 3 personality adjectives. **NEVER** start by drawing.
- **MUST** design in **black and white first**. If it fails in one color, color will not save it.
- **MUST** be legible at **16px** and at 10 metres. Test both.
- **MUST** deliver a variant set: primary (horizontal), stacked, mark-only, and monochrome (black / white / single-color).
- **MUST** define clear space (typically = the height of a key letterform or 1× the mark's x-unit) and a minimum size in px and mm.
- **MUST** deliver vector masters (SVG + PDF) plus generated raster exports; **NEVER** hand a client only a PNG.
- **MUST** check for trademark conflicts and cultural/linguistic issues in the target markets before finalising.
- **NEVER** use gradients, effects, or fine detail as the *only* way the logo works.
- **NEVER** use stock clip-art, an AI-generated raster as a final logo, or a font you have not licensed for commercial use.
- **NEVER** distort, rotate, re-color, add effects to, or place the logo on low-contrast backgrounds — and say so explicitly in the guidelines.

## Version pins / deliverable specs
| Deliverable | Spec |
|---|---|
| Masters | `.svg` (optimised), `.pdf` (vector, outlined text), `.ai`/`.fig` source |
| Raster | PNG @1x/2x/3x on transparent + on white, plus 1024 and 2048 |
| Color spaces | HEX/RGB (screen), CMYK (print), Pantone (spot, if printing) |
| Minimum size | ≥ 24px height for the mark, ≥ 80px width for the horizontal lockup (verify per design) |
| Clear space | ≥ 1× the defined x-unit on all sides |
| Guidelines doc | PDF/Markdown with do/don't visuals |

## Workflow
1. **Brief**: positioning, audience, competitors, 3 personality adjectives, mandatory constraints (colors to avoid, markets, script support).
2. **Audit competitors**: collect 10–20 logos in the category; identify the visual cliché to avoid (every fintech is a blue geometric mark).
3. **Concept, not style**: write 3–5 one-sentence concepts before any visual. Each must be defensible in words.
4. **Sketch broadly** (30+ thumbnails), then narrow to 3 directions.
5. **Construct in vector** on a grid, with geometric relationships (circles, golden/simple ratios), optical corrections applied.
6. **Stress test**: 16px, grayscale, inverted, blurred (squint test), on a photo, embroidered/stamped, in the app icon safe zone, next to competitors.
7. **Build the variant system** and lockups; define clear space and minimum sizes.
8. **Extend the identity**: brand colors (with a full UI-ready ramp handed to `ui-design-system`), typography, imagery style, voice.
9. **Write the guidelines** with correct and incorrect usage examples.
10. **Package** the asset kit with a README and a naming convention.

## Patterns

✅ **Positioning statement (write this first)**
```
For <audience> who <need>, <Brand> is a <category> that <key benefit>,
unlike <alternative>, because <reason to believe>.
Personality: <adjective>, <adjective>, <adjective>.
```

✅ **Variant matrix**
| Variant | Use |
|---|---|
| Primary horizontal (mark + wordmark) | Website header, documents, presentations |
| Stacked | Square placements, social profiles at medium size |
| Mark only | App icon, favicon, avatar, watermark, small sizes |
| Wordmark only | Contexts where the mark is already established |
| Monochrome black | Print, single-color output, engraving |
| Monochrome white (knockout) | Dark/photo backgrounds |

✅ **Asset kit structure**
```
brand/
├── README.md
├── guidelines.pdf
├── logo/
│   ├── svg/{primary,stacked,mark,wordmark}-{color,black,white}.svg
│   ├── pdf/...
│   └── png/{...}@{1x,2x,3x}.png
├── color/palette.json          # HEX, RGB, CMYK, Pantone
├── type/  (licences + webfont files)
└── templates/  (social avatar, cover, letterhead, presentation)
```

❌ **Don't**
```
- A detailed illustration with 8 colors and a gradient, "the logo"
- A wordmark set in an unlicensed display font, never outlined
- Delivering only a 1000×1000 PNG with a white background
- A mark that becomes an unreadable blob at 24px
- "The logo but in the app's accent color" invented ad hoc per screen
```

## Anti-patterns
- Designing the logo before defining the brand — you get decoration, not identification.
- Trend-chasing (this year's flat geometric sans) → dated in 24 months.
- Hidden-meaning gimmicks nobody notices at a glance.
- A mark that only works on white.
- Category clichés: the swoosh, the abstract globe, the handshake, the generic "connection" nodes.
- Ignoring the target script: a Latin-only identity for an Arabic-first product is half a brand.
- No minimum size or clear space rules → the logo gets squeezed into a 12px favicon by someone else.
- Guidelines with only "don'ts" and no rationale — nobody follows rules they don't understand.

## Definition of Done
- [ ] Positioning statement + 3 personality adjectives written and approved.
- [ ] Works in pure black on white and white on black.
- [ ] Legible at 16px and recognisable at 10 metres and when blurred.
- [ ] Full variant set delivered (primary, stacked, mark, wordmark × color/black/white).
- [ ] Clear space and minimum sizes defined and illustrated.
- [ ] Vector masters + generated raster exports + color values for screen and print.
- [ ] Font licences verified for commercial and embedded use; wordmark outlined in masters.
- [ ] Trademark search done in the target jurisdictions; no obvious conflict.
- [ ] Cultural/linguistic check in target markets (symbol meanings, color connotations, name pronunciation).
- [ ] Arabic/second-script lockup produced if the product ships in that market.
- [ ] Guidelines document with do/don't visuals published in the repo.

## References
- `references/logo-construction.md` — concept development, grid construction, optical corrections, stress tests.
- `references/brand-guidelines-template.md` — a fill-in-the-blanks guidelines document.
- `references/arabic-bilingual-branding.md` — Arabic logotypes, bilingual lockups, RTL brand systems.

## ملخص عربي
الشعار نظام تعريف وظيفي لا عمل فني. ابدأ بجملة تموضع وثلاث صفات شخصية قبل الرسم، وصمّم بالأبيض
والأسود أولًا، وتأكد أنه مقروء عند ١٦ بكسل ومن مسافة ١٠ أمتار. سلّم مجموعة متغيرات كاملة (أفقي،
مكدّس، الرمز وحده، أحادي اللون) مع مساحة آمنة وحد أدنى للحجم وملفات فيكتور أصلية، ودليل استخدام
يوضح الممنوع والمسموح. تحقّق من العلامة التجارية والدلالات الثقافية، وأنتج نسخة عربية إن كان
السوق عربيًا.

# Arabic & bilingual branding — reference

An Arabic-market product with a Latin-only identity is half-built. Design both, or design neither.

## 1. Arabic logotype is not a translation
You cannot "set the Arabic name in a font" and call it done. An Arabic logotype is drawn:
- Arabic is cursive — letters **join**, and the joining forms (initial/medial/final/isolated) change shape.
- The baseline is a strong horizontal; ascenders (ا، ل، ك، ط) and descenders (ج، ح، خ، ع، ي، ن، م، و، ر) create the rhythm.
- Never disconnect letters that must join, never letter-space, never stretch (`kashida` must be
  drawn deliberately, not applied by scaling).
- Never apply fake bold or fake italic to Arabic.
- Diacritics (harakat) are usually omitted in logos unless disambiguation is needed.

## 2. Choosing a style
| Style | Character | Use |
|---|---|---|
| Kufi (geometric) | Angular, modern, architectural | Tech, corporate, pairs well with geometric Latin sans |
| Naskh | Classic, readable, traditional | Editorial, institutional, heritage |
| Thuluth / Diwani | Ornate, ceremonial | Luxury, cultural, religious contexts — hard at small sizes |
| Modern/simplified sans | Neutral, contemporary | Products, apps, UI-adjacent branding |

Match the **weight, x-height feel and contrast** of the Latin counterpart, not its letterforms —
imitating Latin shapes in Arabic ("Latinised Arabic") looks amateur to native readers.

## 3. Bilingual lockups

Three valid configurations:

```
1. Stacked (safest)          2. Side by side (mirrored per locale)    3. Locale-specific
   [ mark ]                     العربية  |  Latin                        Arabic version for AR
   Latin                                                                 Latin version for EN
   العربية
```

Rules:
- In RTL contexts, the Arabic reads first (right side / top).
- Both scripts must have **equal optical weight** — Arabic often needs to be set slightly larger
  because its letterforms are optically smaller at the same point size.
- Align on a shared axis (usually the Latin baseline vs. the Arabic baseline, adjusted optically —
  they are not the same line).
- Define the divider (if any) and its clear space as part of the lockup; never let teams improvise.
- Provide separate SVGs per locale rather than expecting anyone to mirror the file.

## 4. The mark itself
- A symbol that reads as a Latin letter (monogram "T") does **not** carry the brand in Arabic.
  Either make the mark abstract/pictorial, or design an Arabic-letter counterpart and define when
  each is used.
- Check that the mark does not resemble an Arabic letter or religious symbol accidentally.
- Mirror-check: mirrored artwork must not produce an unintended shape or word.

## 5. Type pairing for the product
| Latin | Compatible Arabic |
|---|---|
| Inter / Roboto / Helvetica | IBM Plex Sans Arabic, Noto Sans Arabic, Cairo |
| IBM Plex Sans | IBM Plex Sans Arabic (designed as a pair — safest choice) |
| Source Sans | Noto Naskh Arabic |
| Geometric sans (Poppins, Futura-like) | Tajawal, Almarai |

Verify: comparable stroke weight, similar apparent size, and complete weight coverage (many Arabic
fonts lack a true Medium).

## 6. Layout & UI implications
- Mirror the layout: navigation, back arrows, progress, sliders, list chevrons.
- Do **not** mirror: logos, media transport controls, clocks, charts with a fixed numeric axis
  convention (decide per chart), and phone numbers.
- Numerals: choose Western (0-9) or Arabic-Indic (٠-٩) per locale and apply it consistently.
  Most Gulf digital products use Western numerals; Egypt and some markets prefer Arabic-Indic.
- Mixed-direction strings (emails, URLs, brand names inside Arabic sentences) need bidi isolation
  or they render scrambled — use `BidiFormatter`/`\u2068…\u2069`.
- Increase line-height ~10–15% for Arabic body text.
- Arabic text length differs from English by roughly ±30% — never design a layout that only fits
  the English string.

## 7. Cultural checks before launch
- [ ] Name meaning and pronunciation verified by a native speaker in each target dialect.
- [ ] Symbol has no unintended religious, political, or offensive reading.
- [ ] Color connotations checked (green, black, red carry strong local meanings).
- [ ] Imagery appropriate for the market (dress, gender representation, gestures — the thumbs-up
      and the OK sign are not universally positive).
- [ ] Calendar, weekend days (Fri–Sat in several markets), and holidays reflected in product copy.
- [ ] Right-to-left tested on every screen with a real translation, not machine output.

## 8. Deliverables for a bilingual brand
```
brand/logo/svg/
├── primary-en-color.svg      stacked-en-color.svg      mark-color.svg
├── primary-ar-color.svg      stacked-ar-color.svg
├── primary-bilingual.svg     (locked, defined spacing)
└── *-black.svg / *-white.svg for every one of the above
```
Plus: guidance in the guidelines document stating which variant is primary in which market, and
the exact lockup spacing for the bilingual version.

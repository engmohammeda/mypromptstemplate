# The design laws — reference

These are the human-perception rules a senior designer applies unconsciously. Encode them explicitly.

## 1. Gestalt principles (how the eye groups things)

| Principle | Rule in practice |
|---|---|
| **Proximity** | Related items sit closer than unrelated ones. Inner padding < outer padding — always. A label 4dp from its field, 24dp from the next field. |
| **Similarity** | Same function ⇒ same shape, color and size. If two buttons look different, users assume they do different things. |
| **Common region** | A border or a surface tint groups items more strongly than spacing alone. Use one, not both. |
| **Continuity** | Align to a shared axis; the eye follows lines. One left edge per column beats "centred everything". |
| **Closure** | The mind completes shapes — you rarely need full borders; a subtle background is enough. |
| **Figure/ground** | The primary action must be the figure: highest contrast, most saturation, most space around it. |
| **Common fate** | Elements that animate together are perceived as one group. |

**The single most common junior mistake:** equal spacing everywhere, so nothing groups.
Fix: spacing must encode hierarchy (4 / 8 / 16 / 32), never a uniform 16 everywhere.

## 2. Interaction laws

- **Fitts's Law** — time to hit a target ∝ distance / size.
  → Primary actions large and near the thumb (bottom third on mobile); destructive actions small and far.
  → Minimum 48×48dp touch target, 8dp between targets.
- **Hick's Law** — decision time grows with the number of choices.
  → Max 5 primary navigation destinations; progressive disclosure for advanced options; one primary CTA per screen.
- **Miller's Law** — working memory holds ~4–7 chunks.
  → Chunk phone numbers, IBANs, OTP fields; forms in groups of ≤ 7 fields.
- **Jakob's Law** — users expect your app to work like the others they use.
  → Do not reinvent navigation, back behaviour, or standard icon meanings.
- **Doherty Threshold** — keep system response < 400ms or the user disengages.
  → Optimistic UI, skeletons instead of spinners, instant feedback on tap.
- **Tesler's Law** — complexity is conserved; someone must absorb it.
  → Prefer smart defaults in the system over choices pushed to the user.
- **Postel's Law** — be liberal in what you accept (phone formats, dates), strict in what you output.
- **Peak-End Rule** — users remember the peak moment and the end.
  → Invest in the success state and the completion screen, not just the happy path middle.
- **Von Restorff (isolation) effect** — the distinctive item is remembered.
  → Exactly one visually dominant element per screen. Two "primary" buttons = zero primary buttons.
- **Serial position effect** — first and last items are recalled best. Put the most important nav items at the ends.
- **Zeigarnik effect** — incomplete tasks nag. Progress indicators increase completion.
- **Aesthetic-usability effect** — beautiful interfaces are perceived as more usable and their flaws are forgiven — but this is not a licence to skip usability.

## 3. Visual hierarchy — the ordered toolkit
When you need to make something stand out, use these in order (cheapest first):

1. **Position** (top-left in LTR / top-right in RTL, above the fold)
2. **Size** (type scale step, not arbitrary)
3. **Weight** (Medium/SemiBold, rarely Bold everywhere)
4. **Contrast** (foreground vs. surface)
5. **Space** (whitespace around an element is the strongest emphasiser)
6. **Color** (accent — last resort; overuse destroys hierarchy)
7. **Motion** (only for state change, never for decoration)

Rule: if everything is emphasised, nothing is.

## 4. Composition
- **Alignment**: everything aligns to something. Max 2 alignment axes per screen region.
- **Optical vs. mathematical centring**: icons and glyphs often need 1–2dp nudges; trust the eye.
- **Whitespace is a component**, not a leftover. Increase it before adding dividers.
- **Rule of proximity over dividers**: reach for space first, a line second, a card third.
- **Line length** 45–75 characters for readable body text (~ 8–10 words per line on mobile).
- **Density**: pick one (comfortable / compact) per product and apply it consistently.

## 5. Color perception rules
- Blue text on a white background is easier than red; pure saturated colors vibrate — avoid for large areas.
- ~8% of men have some color-vision deficiency: never encode meaning in red/green alone (add icons/labels).
- Warm colors advance, cool recede — use for depth without shadows.
- Saturation attracts attention: keep large surfaces desaturated, save saturation for actions.
- In dark themes, reduce saturation ~20% and raise lightness of accents, or they glow.

## 6. Common "unprofessional look" diagnosis

| Symptom | Cause | Fix |
|---|---|---|
| Looks cluttered | uniform spacing, no grouping | apply proximity: 4/8/16/32 hierarchy |
| Looks cheap | too many saturated colors, default fonts, 3D shadows | one accent, neutral ramp, subtle elevation |
| Looks unfinished | inconsistent alignment and radii | one grid, one radius scale |
| Hard to scan | no hierarchy, all text the same size | apply the type scale; one dominant element |
| Buttons unclear | multiple equally styled CTAs | one primary, others tonal/text |
| Dark mode looks broken | inverted colors | design dark tones deliberately |
| Text hard to read | tight line-height, long lines, low contrast | 1.5 line-height, 45–75 chars, AA contrast |
| Feels slow | no feedback under 400ms | skeletons, optimistic updates, instant press states |

## 7. Review script (apply to any screen)
1. Squint: what do you see first? Is that the intended priority?
2. Grayscale: does hierarchy survive without color?
3. Count: how many font sizes, colors, radii, shadow levels are on screen? (target: ≤ 3, ≤ 4, ≤ 2, ≤ 2)
4. Measure: is every gap on the 4dp grid?
5. Group: does spacing correctly express what belongs together?
6. Contrast-check every text pair.
7. 200% font scale and Arabic RTL: does it still hold?
8. What happens when the data is empty, one item, or 1000 items? Very long name? No network?

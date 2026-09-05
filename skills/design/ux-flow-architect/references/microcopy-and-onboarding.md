# Microcopy — reference

## 1. Voice & tone
Define once, apply everywhere:

| Dimension | Choose |
|---|---|
| Formality | casual ↔ formal |
| Humour | never ↔ occasional (never in errors, payments, health) |
| Person | "you" (yes) / "we" (sparingly) / never "the user" |
| Tense | present, active |
| Length | shortest form that is unambiguous |

Tone **shifts with context**: playful in an empty state, plain in an error, calm in a payment flow.
Never joke while a user is losing data or money.

## 2. Formulas

**Buttons** — verb + object, in the user's terms:
```
✅ Save changes · Send invite · Delete task · Try again · Not now
❌ OK · Submit · Yes · Continue (to what?) · Cancel (cancel what?)
```
Rule: reading only the button, the user should know what will happen.

**Errors** — what + why + what to do:
```
✅ "Couldn't send your message — you're offline. We'll retry when you reconnect."
✅ "That email is already registered. Sign in instead?"  [Sign in]
❌ "Error 500" · "Something went wrong" · "Invalid input"
```
Never blame ("You entered it wrong"), never expose internals, always offer the next step.

**Empty states** — what this is + why it's empty + one action:
```
✅ "No saved articles yet.
    Tap the bookmark icon on any article to keep it here."  [Browse articles]
```

**Confirmations** — name the object and the consequence:
```
✅ "Delete 'Q3 report'? This can't be undone."   [Cancel] [Delete]
❌ "Are you sure?"                                [No] [Yes]
```
Better than a confirmation: do it, then offer **Undo** for 8 seconds.

**Success** — confirm the outcome, not the mechanism:
```
✅ "Invite sent to sara@example.com"     ❌ "Operation completed successfully"
```

**Labels** — nouns the user recognises; never truncate meaning for symmetry.

**Permissions** — benefit first:
```
✅ "Allow notifications to know when your order ships."
❌ "This app would like to send you notifications."
```

## 3. Universal rules
- ≤ 8th-grade reading level. Short sentences. One idea per sentence.
- Sentence case for everything except brand names (easier to scan than Title Case).
- No ALL CAPS for text (blocks screen readers' prosody and hurts Arabic entirely).
- Numbers: numerals ("3 items"), not words.
- Dates: relative for recent ("2 hours ago"), absolute for older ("12 Mar 2026").
- Avoid "please" and "sorry" as filler; use them only when the app genuinely failed the user.
- Never use "simply", "just", "obviously" — they blame the user for finding it hard.
- Placeholder ≠ label. Placeholders disappear and fail accessibility.

## 4. Localisation-safe writing
- **Never concatenate** sentences from fragments: `"You have " + n + " items"` breaks every
  language with plural classes. Use plural resources:
```xml
<plurals name="task_count">
    <item quantity="zero">No tasks</item>
    <item quantity="one">%d task</item>
    <item quantity="two">%d tasks</item>
    <item quantity="few">%d tasks</item>
    <item quantity="many">%d tasks</item>
    <item quantity="other">%d tasks</item>
</plurals>
```
  Arabic uses **all six** plural categories — a two-form English mindset produces broken Arabic.
- Give translators context comments (`<!-- Button on the checkout screen -->`).
- Budget +30–40% length for German/French, and allow for Arabic's different metrics.
- Never embed text in images.
- Avoid idioms, sports metaphors, and culture-bound humour.
- Format numbers, currency, dates with locale-aware APIs, never manually.
- Pseudo-localize early (`Ẋẋ [!!! Ṫḗṡṭ !!!]`) to catch truncation and hardcoded strings.

## 5. Arabic microcopy notes
- Arabic is more formal by default; imperative verbs are fine for buttons ("احفظ", "أرسل").
- Keep button text short — Arabic words are often longer than the English equivalent.
- Avoid transliterated English terms when a common Arabic term exists; but keep well-known technical
  terms (Wi-Fi, PDF) as-is rather than inventing translations.
- Mixed LTR content (emails, URLs, code) inside RTL text needs bidi isolation
  (`\u2068 … \u2069` or `BidiFormatter`) or it renders scrambled.
- Numerals: pick Western or Arabic-Indic per locale and stay consistent app-wide.

## 6. Content checklist per screen
- [ ] Title: what is this screen, in ≤ 4 words.
- [ ] Primary button: verb + object.
- [ ] Every field: visible label + helper text where the format is non-obvious.
- [ ] Every error: cause + fix, attached to the field.
- [ ] Empty state written.
- [ ] Loading state: nothing under 300ms, skeleton after.
- [ ] Success confirmation names the result.
- [ ] All strings externalised as resources with translator comments.
- [ ] Plurals use plural resources, no concatenation.
- [ ] Read aloud: does it sound like a person? Would you say this to a user's face?

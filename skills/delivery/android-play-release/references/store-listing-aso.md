# Store listing & ASO — reference

## 1. Asset specifications

| Asset | Spec | Notes |
|---|---|---|
| App icon | 512×512 PNG, 32-bit, ≤ 1 MB | No alpha for the Play icon; no drop shadow (Play adds it) |
| Feature graphic | 1024×500 PNG/JPG | Shown on the listing and in some placements; keep text minimal and away from edges |
| Phone screenshots | 2–8, 16:9 or 9:16, 320–3840 px per side | First 2–3 are what most users see |
| 7" tablet | up to 8 | Required for tablet quality badge |
| 10" tablet | up to 8 | Required for large-screen recommendations |
| Promo video | YouTube URL | Autoplays muted — must work without sound |
| Title | 30 chars | Brand + one keyword |
| Short description | 80 chars | The single most read line |
| Full description | 4000 chars | Structured, scannable, keyword-natural |
| What's new | 500 chars per release, per locale | Concrete benefits |

## 2. Copy formulas

**Title (30)**: `Brand: Primary Value` — e.g. `Tasky: Focus Timer & Todos`
Never stuff: `Tasky - Best Free Todo List Task Manager Planner 2026` is a policy risk.

**Short description (80)**: one sentence, user outcome first.
> `Plan your day in seconds. Offline tasks, focus timer, and gentle reminders.`

**Full description skeleton**
```
[Hook — 2 lines: the problem and the outcome]

KEY FEATURES
• <Benefit-led feature 1>
• <Benefit-led feature 2>
• <Benefit-led feature 3>

WHY <APP>
<Differentiator vs. alternatives, in plain language>

PRIVACY
<What you collect and what you don't — mirrors the Data safety form>

SUPPORT
<email> · <website>
```
Rules: benefit before feature; no competitor names; no unverifiable claims ("#1", "best");
keywords appear naturally 2–3 times, never as a list.

## 3. Screenshot strategy
1. **Screenshot 1** — the core value in one glance, with a 3–5 word caption.
2. **2–3** — the top two features, each with a caption.
3. **4–6** — differentiators, social proof, breadth.
4. Use real UI with realistic content (never lorem ipsum, never fake data that misleads).
5. Captions: ≥ 24pt equivalent, high contrast, positioned so they survive cropping.
6. Localise captions per language; do **not** ship English captions on an Arabic listing.
7. Keep a device frame optional and consistent; the UI must remain the hero.
8. Generate them automatically (Fastlane `screengrab` / Compose screenshot tests) so they never go stale.

## 4. ASO fundamentals
- Ranking signals you control: title, short description, full description keywords, install
  velocity, retention, ratings, and update cadence.
- Research keywords with real search volume; check what the top 10 competitors rank for.
- Iterate with **store listing experiments (A/B)** in Play Console — one variable at a time,
  run to statistical significance, never eyeball a 2-day result.
- **Custom store listings** per country/audience for meaningful markets.
- Ratings: prompt with the **In-App Review API** after a success moment, never after an error,
  and respect the quota (do not spam).
- Reply to reviews — response rate correlates with rating recovery.

## 5. Localization
- Translate title, descriptions, screenshots captions and what's new — not just the app.
- Arabic: RTL screenshots (the app itself must be RTL-correct), Arabic-Indic vs. Western digits
  chosen consistently, and culturally appropriate imagery.
- Never machine-translate the listing without a native review; bad copy reads as a scam.
- Pseudo-localize the app first (`--pseudo-localize`) to catch truncation before translating.
- Price and currency localisation for paid apps/IAP.

## 6. Pre-launch marketing hooks
- **Pre-registration** campaign for a launch date with a reward.
- Internal/closed track links for beta communities.
- A landing page with the Play badge, privacy policy, support email and the account-deletion URL
  (the last two are Play requirements anyway).

## 7. Listing QA checklist
- [ ] Title ≤ 30 chars, no keyword stuffing, no emoji, no pricing.
- [ ] Short description reads as one clear promise.
- [ ] Full description has no unverifiable superlatives and mirrors the Data safety form.
- [ ] 8 screenshots per form factor, localised, current UI.
- [ ] Feature graphic legible at thumbnail size.
- [ ] Icon consistent with the in-app adaptive icon (see `app-icon-designer`).
- [ ] Video works muted and shows the app within 5 seconds.
- [ ] Privacy policy + support email live.
- [ ] What's new written per locale, benefit-led.
- [ ] Every claim in the listing is true of the shipped build.

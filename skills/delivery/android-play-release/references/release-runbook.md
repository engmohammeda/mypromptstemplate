# Release runbook — reference

## T-7 days — code freeze prep
- [ ] Scope frozen; remaining work moved to the next milestone.
- [ ] `main` green; no known P0/P1 open.
- [ ] Dependency updates merged and soaked for at least 3 days.
- [ ] Compliance checklist (`play-compliance.md`) started.
- [ ] Release notes drafted, translated.

## T-3 days — release candidate
- [ ] Cut branch `release/x.y.z` from `main` (or tag directly if trunk-based).
- [ ] Bump `versionName`; `versionCode` from the CI run number.
- [ ] Full CI run: unit + instrumented + screenshot + benchmark.
- [ ] Build the signed AAB in CI; archive AAB + mapping + symbols.
- [ ] Upload to **internal testing**.
- [ ] Device matrix smoke test (low-end, mid, tablet/foldable, and the oldest supported API).
- [ ] Upgrade test from the current production version.
- [ ] Pre-launch report reviewed.

## T-1 day — go/no-go
- [ ] All checklists complete; declarations updated.
- [ ] Halt criteria and rollback owner agreed **in writing**.
- [ ] Support/CS briefed on what changed.
- [ ] Monitoring dashboards open (Crashlytics, Play vitals, backend error rate).

## T-0 — rollout
1. Promote the internal build to production at **1%**.
2. Wait 4–24 hours. Check: crash-free sessions, ANR rate, new crash clusters, backend 5xx, ratings.
3. 5% → wait 12–24 h → 20% → wait 24 h → 50% → wait 24 h → 100%.
4. Announce internally at each step with the numbers, not "looks fine".

**Halt if:** crash-free < 99.0%, ANR > 0.47%, a new crash cluster in the top 3, a P0 report, or a
sudden 1-star spike.

## Rollback / recovery
Google Play has **no true rollback** — an update cannot be un-shipped from devices that installed it.
Your options, in order:

1. **Halt the staged rollout** (stops further distribution immediately). Do this first, always.
2. **Resume the previous release**: in Play Console, resume the last good release so new installs
   get it. Users already updated stay on the bad version.
3. **Ship a hotfix** — the only real fix for already-updated users:
   - branch from the release tag, cherry-pick the minimal fix, bump patch + `versionCode`,
   - fast-track through CI, internal track verification (still mandatory),
   - rollout at 20% then 100% if healthy.
4. **Server-side kill switch** — the fastest mitigation if you built one (Remote Config flag that
   disables the broken feature without an app update). Build this before you need it.

## Post-release (T+72h)
- [ ] Vitals within thresholds for 72 hours.
- [ ] Crash clusters triaged; issues filed.
- [ ] Reviews scanned for regressions; respond to the top negative ones.
- [ ] Tag pushed, GitHub Release published with notes and artifacts.
- [ ] `CHANGELOG.md` updated.
- [ ] Mapping file archived and confirmed working (deobfuscate one real stack trace).
- [ ] Retro if any halt criterion was hit: what signal was missing, what gate to add.

## Track strategy

| Track | Purpose | Audience |
|---|---|---|
| Internal | Verify the exact Play-signed artifact | ≤ 100 named testers, instant |
| Closed (alpha) | Team/QA + required 20-tester rule for new accounts | Invited lists/groups |
| Open (beta) | Real-world soak, feedback | Anyone who opts in |
| Production | Staged rollout | Everyone |
| Pre-registration | Launch build-up | Interested users |

## Versioning convention
- `MAJOR.MINOR.PATCH` — MAJOR: breaking UX/data change; MINOR: features; PATCH: fixes only.
- `versionCode`: monotonic integer (CI run number or `yyyyMMddHH`). Never reuse.
- Tag format `vMAJOR.MINOR.PATCH`; the tag is the immutable source of the artifact.
- Hotfix from the tag, not from `main`.

## Incident template
```markdown
## Incident: <title>
- Detected: <when, by which signal>
- Impact: <% users, which versions, which flows>
- Root cause:
- Mitigation taken: halt / resume previous / hotfix / kill switch
- Timeline:
- Prevention: <the gate we are adding>
```

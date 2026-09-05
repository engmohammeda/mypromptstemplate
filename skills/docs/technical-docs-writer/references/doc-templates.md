# Document templates — reference

## 1. README

```markdown
# <Project>

> One sentence: what it does and who it's for.

[![Build](badge)](link) [![Coverage](badge)](link) [![License](badge)](link)

## Why this exists
<The problem, in 3 lines.>
**Use it when:** …  **Don't use it when:** …

## Screenshots
| Home | Detail | Dark |
|---|---|---|
| ![](docs/img/home.png) | ![](docs/img/detail.png) | ![](docs/img/dark.png) |

## Quick start
**Prerequisites:** JDK 17 (temurin), Android SDK 36, Git

```bash
git clone https://github.com/org/project.git
cd project
./gradlew assembleDebug
```
**Expected:** `BUILD SUCCESSFUL` and an APK at `app/build/outputs/apk/debug/app-debug.apk`.

## Architecture
<diagram>
- `app/` – entry point and navigation
- `core/*` – shared layers
- `feature/*` – one module per feature
Decisions and their reasoning: [`docs/adr/`](docs/adr/).

## Development
| Task | Command |
|---|---|
| Build | `./gradlew assembleDebug` |
| Unit tests | `./gradlew testDebugUnitTest` |
| All checks | `./gradlew check` |
| Format | `./gradlew ktlintFormat` |
| Release bundle | `./gradlew bundleRelease` |

### Configuration
| Variable | Required | Default | Description |
|---|---|---|---|
| `API_BASE_URL` | yes | — | Backend base URL |

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT © <owner>
```

## 2. ADR

```markdown
# ADR-<NNNN>: <short decision title>

- **Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- **Date:** YYYY-MM-DD
- **Deciders:** @handles

## Context
<Forces at play: constraints, requirements, team, timeline. Facts, not opinions.>

## Decision
<What we will do, in the active voice.>

## Consequences
**Positive:** …
**Negative:** …
**Neutral:** …

## Alternatives considered
| Option | Pros | Cons | Why rejected |
|---|---|---|---|
```
Rules: one decision per ADR, numbered sequentially, **never edited after acceptance** — supersede
it with a new ADR instead. Store in `docs/adr/NNNN-title.md`.

## 3. CONTRIBUTING.md

```markdown
# Contributing

## Setup
<prereqs + clone + build, verified>

## Branching
`main` is always releasable. Work on `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.

## Commits — Conventional Commits
```
<type>(<scope>): <subject>

feat(auth): add biometric unlock
fix(home): prevent crash on empty feed
```
Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.
Breaking changes: `feat(api)!:` or a `BREAKING CHANGE:` footer.

## Pull requests
- One logical change; < 400 lines of diff where possible.
- Description: what, why, how to test, screenshots for UI.
- All checks green: `./gradlew check`.
- At least one approval; CODEOWNERS applies to `build-logic/`, `.github/`.

## Code review checklist
- [ ] Correct and covered by tests
- [ ] No secrets, no debug logging
- [ ] Follows the relevant skill's Non-negotiables
- [ ] Docs/CHANGELOG updated
```

## 4. Runbook (operational)

```markdown
# Runbook: <service / procedure>

## Purpose & when to use
## Prerequisites
Access, tools, credentials (names only, never values).

## Procedure
1. <command>
   Expected: <output>
   If it fails: <recovery>

## Rollback
<exact steps, tested>

## Escalation
| Severity | Contact | Response time |

## Verification
How to confirm the system is healthy afterwards.
```

## 5. Release notes (generated from the changelog)

```markdown
## v2.4.0 — 2026-09-05

### Highlights
- **Offline reading** — saved articles now work with no connection.
- **30% faster startup** on mid-range devices.

### Fixes
- Crash when opening a notification on Android 16 (#245)

### For developers
- Minimum JDK is now 17.
- `ArticleRepository.load()` is deprecated; use `observeArticles()`.

**Full changelog:** v2.3.0...v2.4.0
```
User-facing highlights first, developer details after. Not a raw commit dump.

## 6. GitHub templates

`.github/pull_request_template.md`
```markdown
## What
## Why
## How to test
1.
## Screenshots / recordings
## Checklist
- [ ] Tests added/updated
- [ ] Docs & CHANGELOG updated
- [ ] No secrets committed
- [ ] Verified on a device (UI changes)
```

`.github/ISSUE_TEMPLATE/bug_report.yml`
```yaml
name: Bug report
description: Something is broken
body:
  - type: textarea
    attributes: { label: What happened?, description: Include exact steps }
    validations: { required: true }
  - type: textarea
    attributes: { label: Expected behaviour }
    validations: { required: true }
  - type: input
    attributes: { label: App version }
    validations: { required: true }
  - type: input
    attributes: { label: Device & Android version }
  - type: textarea
    attributes: { label: Logs / stack trace, render: text }
```

## 7. Docs directory layout
```
docs/
├── adr/                 0001-….md
├── flows/               feature flow diagrams (Mermaid)
├── design-system.md
├── architecture.md      Explanation
├── how-to/              task-oriented guides
├── tutorials/           learning-oriented
├── reference/           generated API docs + config tables
├── runbooks/
└── security-review.md
```

# CI hardening, speed and cost — reference

## 1. Permissions & supply chain

```yaml
permissions:
  contents: read          # default for the whole workflow
# escalate per-job only where needed:
jobs:
  release:
    permissions:
      contents: write
```

Rules:
- Set the repository default workflow permission to **read-only** in Settings → Actions.
- Pin third-party actions to a **commit SHA**, not a tag: `uses: foo/bar@a1b2c3d # v1.2.3`.
- Never use `pull_request_target` with `actions/checkout` of the PR head — it gives fork code access to secrets.
- Fork PRs do not receive secrets by design; keep signing jobs off the PR path.
- Enable: secret scanning, push protection, Dependabot alerts, required reviews on `.github/workflows/**` via CODEOWNERS.
- Use **Environments** with required reviewers for anything that publishes.
- Prefer OIDC (`id-token: write`) over long-lived cloud credentials when uploading to GCP/AWS.

## 2. Secrets checklist

| Secret | Purpose |
|---|---|
| `KEYSTORE_BASE64` | `base64 -w0 upload.jks` |
| `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD` | signing |
| `PLAY_SERVICE_ACCOUNT_JSON` | Play publishing (grant only "Release manager" on the specific app) |
| `FIREBASE_APP_ID` / `FIREBASE_TOKEN` | App Distribution |
| `GRADLE_ENCRYPTION_KEY` | configuration-cache encryption for `setup-gradle` |

Never store them at organisation scope if a single repo needs them.

## 3. Speed

| Lever | Effect |
|---|---|
| `gradle/actions/setup-gradle` cache | 3–10× faster dependency resolution |
| `cache-read-only: true` on PR branches | prevents cache thrash; only main writes |
| Split jobs (lint ‖ unit ‖ assemble) | wall-clock ≈ slowest job |
| `--no-daemon` | avoids daemon startup weirdness on ephemeral runners |
| `-Dorg.gradle.workers.max=4` | matches the 4-core standard runner |
| AVD snapshot cache | saves 3–5 min per emulator job |
| `paths-filter` to skip jobs | docs-only PRs skip the build |
| Larger runners | linear cost, sublinear gain — measure before paying |

```yaml
on:
  pull_request:
    paths-ignore: ['**.md', 'docs/**', '.github/ISSUE_TEMPLATE/**']
```

## 4. Reliability
- `timeout-minutes` on **every** job (30 for build, 60 for emulator).
- `fail-fast: false` in matrices so one API level failing still reports the others.
- Retry only genuinely flaky steps (`nick-fields/retry`), never the whole test suite.
- Upload artifacts with `if: always()` so failures are debuggable.
- Add `continue-on-error` **only** to informational jobs (e.g. a size report), never gates.

## 5. Observability
- `$GITHUB_STEP_SUMMARY` for a human-readable run summary (test counts, APK size, coverage).
- Publish JUnit results with `dorny/test-reporter` so failures show inline on the PR.
- Upload lint/detekt SARIF to code scanning.
- Track pipeline duration over time; if the PR gate exceeds 10 minutes, split it.

```yaml
- name: Summary
  if: always()
  run: |
    {
      echo "## Build summary"
      echo "- Variant: debug"
      echo "- Tests: $(grep -o 'tests=\"[0-9]*\"' app/build/test-results/**/*.xml | head -1)"
    } >> "$GITHUB_STEP_SUMMARY"
```

## 6. Cost control
- Public repos: free runners; private repos are billed per minute (macOS 10×, Windows 2×).
- Do not run emulator matrices on every PR; nightly + main is enough for most teams.
- Cancel superseded runs with `concurrency.cancel-in-progress`.
- Set artifact `retention-days` (7 for PR reports, 90 for release artifacts).
- Prune caches: GitHub evicts at 10 GB per repo — keep cache keys tight.

## 7. Branch protection to pair with the pipeline
- Require the PR-check job to pass.
- Require at least one review; CODEOWNERS for `build-logic/`, `.github/`, security-sensitive modules.
- Require linear history and signed commits if your org demands it.
- Block force-push to `main`; tags for releases are immutable.

## 8. Self-hosted runners (only if you must)
- Ephemeral, one job per runner instance; never reuse a runner across untrusted jobs.
- Never enable self-hosted runners on public repositories.
- Keep the Android SDK image pre-baked to save 2–4 minutes per job.

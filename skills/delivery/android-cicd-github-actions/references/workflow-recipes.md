# Workflow recipes — reference

## 1. Release workflow (tag → signed AAB + GitHub Release)

```yaml
name: Release
on:
  push:
    tags: ['v*.*.*']
  workflow_dispatch:
    inputs:
      track:
        description: Play track
        type: choice
        options: [internal, alpha, beta, production]
        default: internal

permissions:
  contents: write   # needed to create the release

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    outputs:
      version: ${{ steps.meta.outputs.version }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - uses: gradle/actions/setup-gradle@v4

      - id: meta
        run: echo "version=${GITHUB_REF_NAME#v}" >> "$GITHUB_OUTPUT"

      - name: Decode keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: |
          echo "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/upload.jks"
          echo "KEYSTORE_PATH=$RUNNER_TEMP/upload.jks" >> "$GITHUB_ENV"

      - name: Build signed bundle and APK
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          VERSION_NAME: ${{ steps.meta.outputs.version }}
          VERSION_CODE: ${{ github.run_number }}
        run: ./gradlew --no-daemon bundleRelease assembleRelease

      - name: Verify signature
        run: |
          $ANDROID_HOME/build-tools/36.0.0/apksigner verify --print-certs \
            app/build/outputs/apk/release/app-release.apk

      - uses: actions/upload-artifact@v4
        with:
          name: release-artifacts
          path: |
            app/build/outputs/bundle/release/*.aab
            app/build/outputs/apk/release/*.apk
            app/build/outputs/mapping/release/mapping.txt
          retention-days: 90

      - name: Shred keystore
        if: always()
        run: rm -f "$RUNNER_TEMP/upload.jks"

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: |
            app/build/outputs/apk/release/*.apk
            app/build/outputs/mapping/release/mapping.txt

  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: production        # protected: requires manual approval
    steps:
      - uses: actions/download-artifact@v4
        with: { name: release-artifacts, path: artifacts }
      - uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.company.app
          releaseFiles: artifacts/bundle/release/app-release.aab
          track: ${{ inputs.track || 'internal' }}
          status: completed
          mappingFile: artifacts/mapping/release/mapping.txt
          whatsNewDirectory: distribution/whatsnew
```

## 2. Reading CI values in Gradle (configuration-cache safe)

```kotlin
val versionNameProvider = providers.environmentVariable("VERSION_NAME").orElse("1.0.0-local")
val versionCodeProvider = providers.environmentVariable("VERSION_CODE").orElse("1")

android {
    defaultConfig {
        versionName = versionNameProvider.get()
        versionCode = versionCodeProvider.get().toInt()
    }
    signingConfigs.create("release") {
        val ks = providers.environmentVariable("KEYSTORE_PATH").orNull
        if (ks != null) {
            storeFile = file(ks)
            storePassword = providers.environmentVariable("KEYSTORE_PASSWORD").get()
            keyAlias = providers.environmentVariable("KEY_ALIAS").get()
            keyPassword = providers.environmentVariable("KEY_PASSWORD").get()
        }
    }
}
```

## 3. Nightly / scheduled quality run

```yaml
name: Nightly
on:
  schedule: [{ cron: '0 2 * * *' }]
  workflow_dispatch:
jobs:
  full-suite:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      # ... setup ...
      - run: ./gradlew --no-daemon check koverXmlReport
      - run: ./gradlew --no-daemon verifyRoborazziDebug
      - name: Benchmark on Firebase Test Lab
        run: |
          gcloud firebase test android run \
            --type instrumentation \
            --app app/build/outputs/apk/release/app-release.apk \
            --test benchmark/build/outputs/apk/androidTest/release/benchmark-release-androidTest.apk \
            --device model=redfin,version=30,locale=en,orientation=portrait \
            --directories-to-pull /sdcard/Download \
            --results-bucket my-benchmark-results
```

## 4. Auto-comment APK size diff on PRs

```yaml
      - name: Size report
        run: |
          SIZE=$(stat -c%s app/build/outputs/apk/debug/app-debug.apk)
          echo "### APK size: $((SIZE/1024/1024)) MB" >> "$GITHUB_STEP_SUMMARY"
```
For a true diff, build the base branch in a second job and compare with a bot comment
(`peter-evans/create-or-update-comment`).

## 5. Dependency & security workflows

```yaml
name: Security
on: [pull_request, schedule]
permissions:
  contents: read
  security-events: write
jobs:
  codeql:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with: { languages: java-kotlin }
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17' }
      - run: ./gradlew assembleDebug
      - uses: github/codeql-action/analyze@v3

  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
```

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: gradle
    directory: "/"
    schedule: { interval: weekly }
    groups:
      androidx: { patterns: ["androidx.*"] }
      kotlin: { patterns: ["org.jetbrains.kotlin*"] }
  - package-ecosystem: github-actions
    directory: "/"
    schedule: { interval: weekly }
```

## 6. Reusable workflow pattern
Put shared steps in `.github/workflows/_android-build.yml` with `on: workflow_call` and inputs
(`gradle-task`, `upload-artifacts`). Call it from PR, main and nightly workflows — one definition,
three triggers.

## 7. Matrix over build variants
```yaml
strategy:
  matrix:
    variant: [freeDebug, paidDebug]
steps:
  - run: ./gradlew assemble${{ matrix.variant }} test${{ matrix.variant }}UnitTest
```

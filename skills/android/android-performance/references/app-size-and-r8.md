# App size & R8 — reference

## 1. Why size matters
Install conversion drops measurably with every extra 10 MB, especially on emerging-market devices.
Optimise **download size** (what Play reports), not the raw APK on disk.

## 2. Baseline configuration

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    packaging {
        resources.excludes += setOf(
            "META-INF/*.kotlin_module", "META-INF/AL2.0", "META-INF/LGPL2.1",
            "DebugProbesKt.bin", "kotlin/**", "**/*.txt", "**/*.version",
        )
    }
    bundle {
        density { enableSplit = true }
        abi { enableSplit = true }
        language { enableSplit = false }   // keep in-app language switcher functional
    }
}
```
`gradle.properties`: `android.enableR8.fullMode=true` (default in AGP 8+).

## 3. R8 keep rules — the discipline

| ✅ Precise | ❌ Over-broad |
|---|---|
| `-keep class com.company.app.model.** { *; }` for reflective serialization | `-keep class ** { *; }` (disables shrinking entirely) |
| `-keepclassmembers class * { @com.google.gson.annotations.SerializedName <fields>; }` | `-dontobfuscate` |
| `-keepnames class com.company.app.api.*Dto` | `-keep class com.google.**` |

Rules you usually need:
```proguard
# Kotlin serialization
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.**
-keepclassmembers class **$$serializer { *; }

# Retrofit / OkHttp
-keepattributes Signature, Exceptions, RuntimeVisibleAnnotations
-keep,allowobfuscation interface <1>
-if interface * { @retrofit2.http.* <methods>; }

# Enums used by name
-keepclassmembers enum * { public static **[] values(); public static ** valueOf(java.lang.String); }

# Crash reporting line numbers
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
```

**Always** test the release build after changing keep rules — R8 bugs surface as
`ClassNotFoundException`/`NoSuchMethodError` only at runtime.

## 4. Where the bytes are

```bash
# APK Analyzer CLI
apkanalyzer apk file-size app-release.apk
apkanalyzer apk download-size app-release.apk
apkanalyzer dex packages --defined-only app-release.apk | sort -k3 -n -r | head -30
apkanalyzer files list app-release.apk | sort -k1 -n -r | head -30

# AAB → device-specific APK size
bundletool build-apks --bundle=app.aab --output=out.apks --mode=default
bundletool get-size total --apks=out.apks
```

## 5. Reduction levers, by typical payoff

| Lever | Typical saving |
|---|---|
| R8 + resource shrinking (if off) | 20–50% |
| PNG → WebP lossless / AVIF | 20–35% of image bytes |
| Vector drawables instead of 5 density PNGs | large |
| Remove unused resources & translations (`resourceConfigurations`) | 5–15% |
| On-demand delivery / dynamic feature modules | varies |
| Play Feature Delivery for rarely-used features | varies |
| Replace a heavy library (e.g. full Firebase BOM → only what's used) | varies |
| `Play Asset Delivery` for large assets | moves bytes out of the base |
| Drop legacy ABIs (`armeabi-v7a` only if data supports it) | ~40% of native bytes |

## 6. Size gate in CI

```yaml
- name: Check AAB size
  run: |
    SIZE=$(stat -c%s app/build/outputs/bundle/release/app-release.aab)
    MAX=$((25 * 1024 * 1024))
    echo "AAB size: $((SIZE/1024/1024)) MB"
    if [ "$SIZE" -gt "$MAX" ]; then echo "::error::AAB exceeds 25 MB budget"; exit 1; fi
```
Better: post a diff comment vs. the base branch so growth is visible in review.

## 7. Mapping & deobfuscation
- Upload `app/build/outputs/mapping/release/mapping.txt` to Play (automatic with AAB) and to your
  crash reporter, every release. Without it, every stack trace is garbage.
- Archive the mapping file as a CI artifact and in the GitHub Release.
- Native code: upload `.so` debug symbols (`android.buildTypes.release.ndk.debugSymbolLevel = "FULL"`).

## 8. Checklist
- [ ] `isMinifyEnabled` + `isShrinkResources` on, R8 full mode.
- [ ] Release build smoke-tested on a device (obfuscation crashes only show at runtime).
- [ ] No `-keep class **` wildcards.
- [ ] All raster images WebP/AVIF; icons are vectors.
- [ ] Unused translations removed.
- [ ] Download size measured with `bundletool`, within budget.
- [ ] Mapping + native symbols uploaded.

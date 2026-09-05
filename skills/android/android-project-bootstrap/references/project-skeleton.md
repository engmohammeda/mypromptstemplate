# Project skeleton — reference

## Directory tree

```
myapp/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle.properties
├── gradle/
│   ├── libs.versions.toml
│   └── wrapper/{gradle-wrapper.jar,gradle-wrapper.properties}
├── build-logic/
│   ├── settings.gradle.kts
│   └── convention/
│       ├── build.gradle.kts
│       └── src/main/kotlin/
│           ├── AndroidApplicationConventionPlugin.kt
│           ├── AndroidLibraryConventionPlugin.kt
│           ├── AndroidComposeConventionPlugin.kt
│           ├── AndroidHiltConventionPlugin.kt
│           └── com/company/app/KotlinAndroid.kt
├── app/
│   └── src/{main,debug,test,androidTest}/
├── core/
│   ├── common/        # Result wrappers, dispatchers, extensions
│   ├── model/         # pure Kotlin domain models
│   ├── domain/        # use cases (pure Kotlin)
│   ├── data/          # repositories, mappers
│   ├── database/      # Room
│   ├── network/       # Retrofit/Ktor
│   ├── datastore/     # Preferences/Proto
│   ├── designsystem/  # theme, tokens, atoms
│   ├── ui/            # shared composables bound to domain models
│   └── testing/       # test doubles, rules, fixtures
├── feature/
│   ├── home/
│   ├── auth/
│   └── settings/
└── docs/adr/
```

**Dependency rule:** `app → feature → core:ui → core:designsystem`, `feature → core:domain → core:model`.
`core:data` implements interfaces declared in `core:domain`. Features **never** depend on each other.

## settings.gradle.kts

```kotlin
pluginManagement {
    includeBuild("build-logic")
    repositories {
        google { content { includeGroupByRegex("com\\.android.*|com\\.google.*|androidx.*") } }
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories { google(); mavenCentral() }
}

enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

rootProject.name = "myapp"
include(":app")
include(":core:common", ":core:model", ":core:domain", ":core:data", ":core:database",
        ":core:network", ":core:designsystem", ":core:ui", ":core:testing")
include(":feature:home", ":feature:auth", ":feature:settings")
```

## gradle.properties

```properties
org.gradle.jvmargs=-Xmx4g -XX:+HeapDumpOnOutOfMemoryError -XX:MaxMetaspaceSize=1g -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.configureondemand=false

android.useAndroidX=true
android.nonTransitiveRClass=true
android.nonFinalResIds=true
android.defaults.buildfeatures.buildconfig=false
android.defaults.buildfeatures.resvalues=false

kotlin.code.style=official
kotlin.incremental=true
ksp.incremental=true
```

## build-logic/convention — Android library plugin

```kotlin
class AndroidLibraryConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        pluginManager.apply("com.android.library")

        extensions.configure<LibraryExtension> {
            compileSdk = 36
            defaultConfig {
                minSdk = 24
                testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
                consumerProguardFiles("consumer-rules.pro")
            }
            compileOptions {
                sourceCompatibility = JavaVersion.VERSION_17
                targetCompatibility = JavaVersion.VERSION_17
                isCoreLibraryDesugaringEnabled = true
            }
            buildTypes {
                release { isMinifyEnabled = false }
            }
            testOptions.unitTests {
                isIncludeAndroidResources = true
                isReturnDefaultValues = true
            }
        }
        extensions.configure<KotlinAndroidProjectExtension> {
            jvmToolchain(17)
            compilerOptions {
                allWarningsAsErrors.set(true)
                freeCompilerArgs.addAll("-Xjvm-default=all", "-opt-in=kotlin.RequiresOptIn")
            }
        }
        dependencies {
            add("coreLibraryDesugaring", libs.findLibrary("desugar.jdk.libs").get())
        }
    }
}
```

Register in `build-logic/convention/build.gradle.kts`:

```kotlin
gradlePlugin {
    plugins {
        register("androidLibrary") {
            id = "myapp.android.library"
            implementationClass = "AndroidLibraryConventionPlugin"
        }
    }
}
```

## app/build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.myapp.android.application)
    alias(libs.plugins.myapp.android.compose)
    alias(libs.plugins.myapp.android.hilt)
}

android {
    namespace = "com.company.app"
    defaultConfig {
        applicationId = "com.company.app"
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }
    signingConfigs {
        create("release") {
            storeFile = System.getenv("KEYSTORE_PATH")?.let(::file)
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        debug { applicationIdSuffix = ".debug"; isDebuggable = true }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    bundle {
        language { enableSplit = false }   // keep in-app language switching working
    }
}
```

## .gitignore essentials

```gitignore
*.iml
.gradle/
/local.properties
/.idea/
.DS_Store
/build
*/build
/captures
.externalNativeBuild
.cxx
*.jks
*.keystore
keystore.properties
google-services.json
/app/release/
```

## Starter quality config

`config/detekt/detekt.yml` — start from `detekt --generate-config`, then set
`build.maxIssues: 0`, enable `formatting` ruleset via `detekt-formatting`, and
`complexity.LongMethod.threshold: 40`.

`.editorconfig`:
```ini
root = true
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
max_line_length = 120
[*.{yml,yaml,json,toml}]
indent_size = 2
```

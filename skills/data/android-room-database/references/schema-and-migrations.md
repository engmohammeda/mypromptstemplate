# Schema & migrations — reference

## 1. Enabling schema export (KSP)

```kotlin
ksp { arg("room.schemaLocation", "$projectDir/schemas") }

android {
    sourceSets["androidTest"].assets.srcDir("$projectDir/schemas")
    defaultConfig {
        // required so MigrationTestHelper can read them
    }
}
dependencies {
    implementation(libs.room.runtime)
    implementation(libs.room.ktx)
    ksp(libs.room.compiler)
    androidTestImplementation(libs.room.testing)
}
```
Commit `schemas/com.company.app.AppDatabase/1.json`, `2.json`, … They are the migration contract.

## 2. Modelling rules

| Decision | Rule |
|---|---|
| Primary key | Stable, server-provided id when available; otherwise UUID. Avoid autoincrement for synced data |
| Column names | `snake_case` via `@ColumnInfo(name=)`; Kotlin properties stay camelCase |
| Booleans | `INTEGER NOT NULL DEFAULT 0` |
| Dates | Store epoch millis (`Long`) or ISO-8601 text; **pick one and never mix** |
| Enums | `@TypeConverter` to `String` (name), never ordinal — reordering the enum corrupts data |
| Nullability | Model the truth; `NOT NULL` with a default is better than nullable |
| Relations | Real foreign keys with `onDelete = CASCADE`; `@Relation` for reads |
| Many-to-many | Junction entity with a composite primary key |
| Sync metadata | `updated_at`, `synced_at`, `is_dirty` columns for offline-first |

```kotlin
@Entity(primaryKeys = ["article_id", "tag_id"], tableName = "article_tags")
data class ArticleTagCrossRef(
    @ColumnInfo(name = "article_id") val articleId: String,
    @ColumnInfo(name = "tag_id") val tagId: String,
)

data class ArticleWithTags(
    @Embedded val article: ArticleEntity,
    @Relation(
        parentColumn = "id", entityColumn = "id",
        associateBy = Junction(ArticleTagCrossRef::class,
            parentColumn = "article_id", entityColumn = "tag_id"),
    )
    val tags: List<TagEntity>,
)
```
DAO methods returning `@Relation` types must be annotated `@Transaction` (Room runs multiple queries).

## 3. Migration recipes

**Add a column**
```sql
ALTER TABLE articles ADD COLUMN is_bookmarked INTEGER NOT NULL DEFAULT 0;
```

**Drop / rename a column, change a type, or change constraints** — SQLite cannot do it directly.
Use the create-copy-drop-rename dance:
```kotlin
override fun migrate(db: SupportSQLiteDatabase) {
    db.execSQL("""
        CREATE TABLE articles_new (
            id TEXT NOT NULL PRIMARY KEY,
            remote_id INTEGER NOT NULL,
            author_id TEXT NOT NULL,
            title TEXT NOT NULL,
            published_at INTEGER NOT NULL,
            is_bookmarked INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE
        )
    """.trimIndent())
    db.execSQL("""
        INSERT INTO articles_new (id, remote_id, author_id, title, published_at)
        SELECT id, remote_id, author_id, title, published_at FROM articles
    """.trimIndent())
    db.execSQL("DROP TABLE articles")
    db.execSQL("ALTER TABLE articles_new RENAME TO articles")
    db.execSQL("CREATE UNIQUE INDEX index_articles_remote_id ON articles(remote_id)")
    db.execSQL("CREATE INDEX index_articles_published_at ON articles(published_at)")
}
```
Indices are **not** carried over by rename — recreate every one.

**AutoMigration** (for simple, unambiguous changes):
```kotlin
@Database(
    entities = [ArticleEntity::class],
    version = 5,
    autoMigrations = [
        AutoMigration(from = 4, to = 5, spec = AppDatabase.RenameTitleSpec::class),
    ],
    exportSchema = true,
)
abstract class AppDatabase : RoomDatabase() {
    @RenameColumn(tableName = "articles", fromColumnName = "title", toColumnName = "headline")
    class RenameTitleSpec : AutoMigrationSpec
}
```
Auto-migrations still require exported schemas and still deserve a test.

## 4. Migration test harness

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    private val TEST_DB = "migration-test"

    @get:Rule
    val helper = MigrationTestHelper(
        InstrumentationRegistry.getInstrumentation(),
        AppDatabase::class.java,
        emptyList(),
        FrameworkSQLiteOpenHelperFactory(),
    )

    @Test fun migrateAll() {
        helper.createDatabase(TEST_DB, 1).close()
        Room.databaseBuilder(
            InstrumentationRegistry.getInstrumentation().targetContext,
            AppDatabase::class.java, TEST_DB,
        ).addMigrations(*ALL_MIGRATIONS).build().apply {
            openHelper.writableDatabase.close()
        }
    }
}
```
`migrateAll` catches the classic bug: each pairwise migration works, but the full 1→N chain breaks.

## 5. Destructive fallback policy
Allowed **only** for:
- debug builds, and
- a pure cache database whose loss is invisible to the user (and then use
  `fallbackToDestructiveMigrationFrom(...)` for specific versions, not blanket).

Everything else: write the migration.

## 6. Multi-database strategy
Split databases when data has different lifecycles:
- `app.db` — user data (must migrate carefully, backed up).
- `cache.db` — network cache (destructive fallback is fine, excluded from backup).

Never join across databases in SQL; join in Kotlin at the repository level, or keep them together.

## 7. Pre-populated databases
```kotlin
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .createFromAsset("database/seed.db")
    .addMigrations(*ALL_MIGRATIONS)
    .build()
```
The asset's `user_version` must match the `@Database(version=)` you claim it is.

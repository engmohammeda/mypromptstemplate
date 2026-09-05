---
name: android-room-database
description: >-
  Designs, implements and migrates Android local persistence with Room and SQLite: schema and
  entity modelling, relations, indices, DAO queries with Flow, transactions, migrations and
  migration tests, encryption, and query performance. Use when the user mentions Room, SQLite,
  DAO, @Entity, @Query, database migration, fallbackToDestructiveMigration, schema, indices,
  local cache, offline storage, DataStore vs database, or asks to design or fix an Android database.
version: 1.0.0
license: MIT
category: data
tags: [android, room, sqlite, database, migrations, persistence, offline]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
metadata:
  maturity: stable
  arabic_summary: "تصميم وتنفيذ قواعد بيانات Room/SQLite على أندرويد مع الهجرات والاختبارات وضبط الأداء."
---

# Android Room Database

You are the data engineer. The database is the app's **single source of truth** — schema mistakes
are permanent, because users' devices already have the old one.

## When to use
- Designing local storage for an offline-first app.
- Writing entities, DAOs, relations, queries, migrations.
- Debugging slow queries, main-thread DB access, or migration crashes.

## When NOT to use
- Key-value settings/preferences → use **DataStore**, not Room.
- Repository/threading design → `android-kotlin-architecture`.

## Non-negotiables
- **MUST** export schemas (`room.schemaLocation`) and **commit** the JSON files. Migrations cannot be tested without them.
- **MUST** write and test a `Migration` for every schema change shipped to production. **NEVER** use `fallbackToDestructiveMigration()` in release — it silently deletes user data.
- **MUST** keep entities separate from domain models; map at the data layer boundary.
- **MUST** return `Flow<T>` for observation and `suspend` for one-shot operations. **NEVER** run a query on the main thread (`allowMainThreadQueries()` is test-only).
- **MUST** index every column used in `WHERE`, `JOIN`, or `ORDER BY`, and every foreign key.
- **MUST** wrap multi-statement writes in `@Transaction`.
- **MUST** use KSP (not KAPT) for the Room compiler.
- **NEVER** store large blobs (images, files) in the database — store a file path/URI.
- **NEVER** use `SELECT *` in a query returning a projection class you control; select the columns you need.
- **NEVER** expose `LiveData`/`Cursor` above the data layer.

## Version pins
| Component | Version |
|---|---|
| Room | 2.9.x (KSP) |
| SQLite (bundled, optional) | androidx.sqlite bundled driver |
| SQLCipher (if encrypting) | 4.x |
| Paging | 3.4.x |

## Workflow
1. **Model the data**: entities, relations (1-1, 1-N, N-M via a junction table), keys, nullability. Normalise first; denormalise only with a measured reason.
2. **Decide the storage**: Room for relational/queryable data; DataStore for < ~100 scalar settings; files for media.
3. **Write entities** with explicit `tableName`, `@ColumnInfo(name = ...)`, indices and foreign keys.
4. **Write DAOs**: `Flow` reads, `suspend` writes, `@Upsert`, `@Transaction` for compound operations, paging sources where lists are long.
5. **Enable schema export** and commit `schemas/<db>/1.json`.
6. **Every change afterwards**: bump `version`, add a `Migration(n, n+1)`, add a `MigrationTestHelper` test, commit the new schema JSON.
7. **Add integration tests** with an in-memory database (see `android-testing-quality`).
8. **Profile**: `EXPLAIN QUERY PLAN`, Database Inspector, and check for full table scans.

## Patterns

✅ **Entity with index and foreign key**
```kotlin
@Entity(
    tableName = "articles",
    indices = [
        Index(value = ["author_id"]),
        Index(value = ["published_at"]),
        Index(value = ["remote_id"], unique = true),
    ],
    foreignKeys = [ForeignKey(
        entity = AuthorEntity::class,
        parentColumns = ["id"],
        childColumns = ["author_id"],
        onDelete = ForeignKey.CASCADE,
    )],
)
data class ArticleEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "remote_id") val remoteId: Long,
    @ColumnInfo(name = "author_id") val authorId: String,
    val title: String,
    @ColumnInfo(name = "published_at") val publishedAt: Long,
    @ColumnInfo(defaultValue = "0") val isBookmarked: Boolean,
)
```

✅ **DAO**
```kotlin
@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles ORDER BY published_at DESC")
    fun observeAll(): Flow<List<ArticleEntity>>

    @Query("SELECT * FROM articles WHERE author_id = :authorId ORDER BY published_at DESC LIMIT :limit")
    fun observeByAuthor(authorId: String, limit: Int = 50): Flow<List<ArticleEntity>>

    @Upsert
    suspend fun upsertAll(articles: List<ArticleEntity>)

    @Query("DELETE FROM articles WHERE published_at < :cutoff")
    suspend fun deleteOlderThan(cutoff: Long): Int

    @Transaction
    suspend fun replaceAll(articles: List<ArticleEntity>) {
        clear()
        upsertAll(articles)
    }

    @Query("DELETE FROM articles")
    suspend fun clear()
}
```

✅ **Migration + test**
```kotlin
val MIGRATION_3_4 = object : Migration(3, 4) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE articles ADD COLUMN is_bookmarked INTEGER NOT NULL DEFAULT 0")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_articles_published_at ON articles(published_at)")
    }
}

@Test
fun migrate3To4_preservesRows() {
    helper.createDatabase(TEST_DB, 3).apply {
        execSQL("INSERT INTO articles (id, remote_id, author_id, title, published_at) VALUES ('1', 1, 'a', 't', 0)")
        close()
    }
    val db = helper.runMigrationsAndValidate(TEST_DB, 4, true, MIGRATION_3_4)
    db.query("SELECT is_bookmarked FROM articles WHERE id = '1'").use {
        assertThat(it.moveToFirst()).isTrue()
        assertThat(it.getInt(0)).isEqualTo(0)
    }
}
```

❌ **Don't**
```kotlin
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .allowMainThreadQueries()            // blocks the UI
    .fallbackToDestructiveMigration()    // deletes user data on every schema bump
    .build()

@Query("SELECT * FROM articles WHERE title LIKE '%' || :q || '%'")  // full scan, no FTS
fun search(q: String): List<ArticleEntity>
```

## Anti-patterns
- One `AppDatabase` god-class shared across unrelated features with 40 entities and no ownership.
- Storing JSON blobs in a column and filtering them in Kotlin instead of modelling columns.
- `@TypeConverter` for complex objects that should be their own table.
- Nullable everything "to be safe" — nullability is part of the schema contract.
- Reading the whole table to compute a count (`SELECT COUNT(*)` exists).
- Deleting and reinserting entire tables on every sync instead of upserting deltas.
- Ignoring `onConflict` strategy and getting silent duplicate rows.
- Using `LIKE '%term%'` for search instead of an FTS4/FTS5 virtual table.

## Definition of Done
- [ ] Schema JSONs exported and committed for every version.
- [ ] Migration written **and** tested for each version bump; no destructive fallback in release.
- [ ] All queries observed as `Flow`; writes are `suspend`; nothing on the main thread.
- [ ] Indices cover every filter/sort/join column; verified with `EXPLAIN QUERY PLAN`.
- [ ] Entities never leave the data layer.
- [ ] DAO integration tests cover insert/update/delete/conflict/relation paths.
- [ ] Upgrade tested end-to-end: install the previous release, then the new build, data intact.
- [ ] Encryption applied if the data is sensitive.

## References
- `references/schema-and-migrations.md` — modelling rules, migration recipes, testing setup.
- `references/query-performance.md` — indexing, EXPLAIN, FTS, paging, transactions, encryption.
- Room docs: https://developer.android.com/training/data-storage/room

## ملخص عربي
قاعدة البيانات هي مصدر الحقيقة الوحيد، وأي خطأ في المخطط يبقى على أجهزة المستخدمين. لذلك: صدّر
ملفات المخطط واحفظها في Git، واكتب هجرة مختبَرة لكل تغيير، وممنوع منعًا باتًا
`fallbackToDestructiveMigration` في الإصدار. القراءة عبر `Flow` والكتابة `suspend`، وفهارس على كل
عمود يُستخدم في التصفية أو الترتيب أو الربط، ولا تُسرَّب كيانات Room خارج طبقة البيانات.

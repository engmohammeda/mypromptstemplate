# Query performance, search & encryption — reference

## 1. Indexing rules
Index a column when it appears in `WHERE`, `JOIN … ON`, `ORDER BY`, or `GROUP BY`.

- Composite index column order matters: `Index(value = ["author_id", "published_at"])` serves
  `WHERE author_id = ? ORDER BY published_at` — the reverse order does not.
- Every foreign key needs an index (Room warns if missing).
- Unique constraints double as indices — do not duplicate them.
- Cost: each index slows writes and grows the file. Do not index low-cardinality flags alone.

## 2. Read the plan
```bash
adb shell "run-as com.company.app sqlite3 databases/app.db 'EXPLAIN QUERY PLAN
  SELECT * FROM articles WHERE author_id = \"a\" ORDER BY published_at DESC;'"
```
- `SEARCH articles USING INDEX index_articles_author_id` → good.
- `SCAN articles` on a large table → missing index.
- `USE TEMP B-TREE FOR ORDER BY` → the sort is not index-backed.

Use the **Database Inspector** in Android Studio for live queries during development.

## 3. Query hygiene

| ❌ | ✅ |
|---|---|
| `SELECT *` then map 3 fields | projection `data class` + explicit columns |
| Load all rows, filter in Kotlin | filter in SQL with `WHERE`/`LIMIT` |
| `COUNT` by loading the list | `SELECT COUNT(*)` |
| N+1 queries in a loop | one query with `IN (:ids)` or `@Relation` |
| `LIKE '%term%'` | FTS4/FTS5 virtual table |
| Insert in a loop | `@Insert(list)` inside a `@Transaction` (10–100× faster) |

Projection example:
```kotlin
data class ArticleListItem(
    val id: String,
    val title: String,
    @ColumnInfo(name = "published_at") val publishedAt: Long,
)

@Query("SELECT id, title, published_at FROM articles ORDER BY published_at DESC")
fun observeListItems(): Flow<List<ArticleListItem>>
```

## 4. Full-text search
```kotlin
@Fts4(contentEntity = ArticleEntity::class)
@Entity(tableName = "articles_fts")
data class ArticleFts(
    val title: String,
    val body: String,
)

@Query("""
    SELECT a.* FROM articles a
    JOIN articles_fts f ON f.rowid = a.rowid
    WHERE articles_fts MATCH :query
    ORDER BY a.published_at DESC
""")
fun search(query: String): Flow<List<ArticleEntity>>
```
Sanitise the user query (escape `"` and operators) before passing it to `MATCH`.
For Arabic content, normalise diacritics and Alef variants (`أإآ` → `ا`) into a separate
`normalized_title` column before indexing.

## 5. Transactions
```kotlin
@Transaction
suspend fun syncArticles(remote: List<ArticleEntity>, deletedIds: List<String>) {
    upsertAll(remote)
    deleteByIds(deletedIds)
}
```
- One transaction per logical unit; not per row.
- Room's `withTransaction { }` for suspend blocks spanning multiple DAOs.
- Long transactions block other writers — keep them short and never do network I/O inside one.

## 6. Paging 3 integration
```kotlin
@Query("SELECT * FROM articles ORDER BY published_at DESC")
fun pagingSource(): PagingSource<Int, ArticleEntity>
```
Room invalidates the `PagingSource` automatically on writes. Pair with a `RemoteMediator` for
network-backed pagination, and always `cachedIn(viewModelScope)`.

## 7. Encryption at rest (SQLCipher)
```kotlin
val passphrase = SQLiteDatabase.getBytes(keyFromKeystore)
val factory = SupportFactory(passphrase)

Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .openHelperFactory(factory)
    .addMigrations(*ALL_MIGRATIONS)
    .build()
```
- The passphrase must come from the **Android Keystore**, never a constant.
- Encryption costs roughly 5–15% on reads — measure before adopting it for non-sensitive data.
- Encrypted databases cannot be inspected with Database Inspector; keep a debug flavour unencrypted.
- Plan the migration path: an existing plaintext DB must be re-encrypted (`sqlcipher_export`).

## 8. Backup & privacy
```xml
<application
    android:allowBackup="true"
    android:dataExtractionRules="@xml/data_extraction_rules">
```
```xml
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="database" path="cache.db" />
        <exclude domain="sharedpref" path="auth.xml" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="database" path="cache.db" />
    </device-transfer>
</data-extraction-rules>
```

## 9. Performance budgets
| Operation | Budget |
|---|---|
| Single-row read by primary key | < 1 ms |
| List query (50 rows, indexed) | < 10 ms |
| Bulk upsert (1000 rows, one transaction) | < 200 ms |
| Database open + migration on upgrade | < 500 ms |
| Main-thread DB time | 0 ms — always |

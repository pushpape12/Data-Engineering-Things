# Apache Iceberg and open table formats: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Parquet versus Iceberg
2. Catalog and partition transforms
3. Snapshots, maintenance and recovery

## 1. Parquet versus Iceberg

### Understand it

Parquet is a file format. Iceberg is a table format that organizes files through metadata and snapshots. A catalog resolves a table's current metadata; the engine reads the selected snapshot rather than whichever objects happen to be listed at a path.

### Practical example

```text
catalog -> table metadata -> snapshot -> manifests -> data/delete files
Parquet -> physical columnar file contents
```

**Expected result and reasoning:** Two readers selecting the same snapshot see the same logical table, subject to compatible engines and retained files.

### Interview question

**Why is a directory of Parquet files not automatically an ACID table?**

It lacks the table's coordinated metadata/commit protocol and snapshot model. Concurrent file replacement or directory listing can expose partial updates without an appropriate transactional layer.

**Common mistake:** Using the table format name as if it were a storage service or compute engine.

**Try it yourself:** Explain the role of catalog, object store and Spark separately.

## 2. Catalog and partition transforms

### Understand it

An Iceberg catalog identifies tables and commits metadata updates. Hidden partition transforms let the engine map filters to storage partitioning without requiring users to manually filter a derived directory column. Runtime/catalog configuration must match the engine.

### Practical example

```sql
-- Template with preconfigured local catalog/learning namespace:
CREATE TABLE local.learning.order_events (
 order_id BIGINT,event_time TIMESTAMP,amount_cents BIGINT
) USING iceberg PARTITIONED BY (days(event_time));
```

**Expected result and reasoning:** This creates a table partitioned by a day transform in a compatible environment. No table is created by merely reading this guide.

### Interview question

**What is partition evolution useful for?**

It changes how new data is partitioned without pretending old files were physically rewritten. Compatible engines use table metadata to interpret the relevant partition specifications.

**Common mistake:** Assuming a new partition specification instantly reorganizes all old data.

**Try it yourself:** Compare changing day partitions to hour partitions on new writes versus rewriting history.

## 3. Snapshots, maintenance and recovery

### Understand it

Each committed snapshot identifies table state. Compaction addresses physical layout; snapshot expiration and orphan cleanup address retention/storage with different risks. Readers and rollback requirements determine safe retention windows.

### Practical example

```sql
-- Existing Iceberg table, compatible Spark catalog:
SELECT committed_at,snapshot_id FROM local.learning.orders.snapshots;
```

**Expected result and reasoning:** Inspect real snapshot history before deciding cleanup. The query requires the earlier configured table; it is not a maintenance operation.

### Interview question

**How can cleanup break a long-running reader?**

Removing files still required by its snapshot can make reads fail. Account for reader lifetime, branch/tag retention and rollback objectives, and use supported maintenance procedures.

**Common mistake:** Deleting objects manually based only on modification time.

**Try it yourself:** Design maintenance around a 24-hour maximum reader lifetime and seven-day rollback objective.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

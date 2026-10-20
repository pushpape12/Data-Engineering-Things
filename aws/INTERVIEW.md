# AWS data engineering: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. S3 layout and partition pruning
2. Glue catalog, Glue jobs and EMR
3. Athena and cost-aware SQL
4. Lambda and duplicate delivery
5. Job bookmarks and source watermarks

## 1. S3 layout and partition pruning

### Understand it

S3 stores objects by key. A prefix convention helps query engines discover/filter partitions, but a prefix alone does not create catalog metadata or guarantee engine pruning. Partition by common bounded filters and avoid high-cardinality fragmentation.

### Practical example

```text
raw/orders/ingest_date=2026-10-01/batch-001.jsonl
curated/orders/order_date=2026-10-01/part-000.parquet
```

**Expected result and reasoning:** Ingest date supports arrival auditing; order date supports business reporting. A late order can have different values for those dates.

### Interview question

**Why does a date filter still scan too much data?**

Check catalog/table partition definitions, predicate types, layout and actual scan metrics. A function or cast, missing metadata or unsuitable physical organization may prevent the intended pruning.

**Common mistake:** Treating S3 key prefixes as database indexes.

**Try it yourself:** Plan how to rebuild one business-date partition containing late arrivals.

## 2. Glue catalog, Glue jobs and EMR

### Understand it

A catalog describes data; execution engines transform it. Glue jobs provide managed ETL execution, while EMR options expose other managed Spark/Hadoop application choices. Select runtime, dependency packaging and scaling based on the workload rather than assuming all services run identical binaries.

### Practical example

```text
S3 objects -> Glue Catalog table -> Athena query
S3 objects -> Glue Spark job -> curated Parquet
S3 objects -> EMR Serverless Spark application -> curated Parquet
```

**Expected result and reasoning:** The catalog is metadata, not a worker that executes the transformation. The compute choice is independent of that role.

### Interview question

**Glue or EMR Serverless: how do you choose?**

Compare supported runtime/features, dependency requirements, startup latency, operational integration and measured cost/performance. Use a representative job and the actual deployment constraints.

**Common mistake:** Claiming the crawler validates every row's business meaning.

**Try it yourself:** List the Python/JAR compatibility checks needed before a Spark runtime upgrade.

## 3. Athena and cost-aware SQL

### Understand it

Athena queries data through configured table metadata. Columnar storage, selective columns and partition predicates can reduce scanning. Cost depends on the configured capacity/pricing model; inspect scan statistics rather than quoting a universal price.

### Practical example

```sql
-- Template: existing Athena table with DATE partition column order_date.
SELECT customer_id,SUM(amount_cents) AS revenue
FROM curated_orders
WHERE order_date=DATE '2026-10-01'
GROUP BY customer_id;
```

**Expected result and reasoning:** Expected totals depend on the destination dataset; with the shared current-state fixture, 101=450 and 102=250. Requires existing S3/catalog/results configuration.

### Interview question

**How would you reduce a large Athena scan?**

Check projection and partition pruning, convert row-oriented data to columnar when suitable, compact tiny files and review query frequency. Preserve correctness and compare bytes scanned on equivalent queries.

**Common mistake:** Using LIMIT as a guaranteed reduction in bytes scanned.

**Try it yourself:** Compare a SELECT * query with the two-column aggregate and inspect actual scan metrics.

## 4. Lambda and duplicate delivery

### Understand it

Event-driven processing can repeat messages and invoke functions concurrently. A durable idempotency record needs ownership/expiry semantics, while the destination must tolerate crashes between claim, write and completion. A process-local set is insufficient.

### Practical example

```text
event e1 claimed -> sink commits -> function crashes
retry e1 -> consult durable state + idempotent sink -> one logical result
```

**Expected result and reasoning:** A completed sink write remains safe when delivery repeats. A claim stuck in progress needs an explicit recovery rule.

### Interview question

**How do you prevent duplicate S3-triggered processing?**

Use a stable source identity including version where appropriate, conditional durable claims, replay-safe output and recovery for interrupted claims. Bound concurrency and distinguish retryable from invalid records.

**Common mistake:** Using only the object key when overwrites create distinct object versions.

**Try it yourself:** Draw the crash points around a claim, sink write and status update.

## 5. Job bookmarks and source watermarks

### Understand it

Glue bookmarks track supported source progress, not business-level exactly-once output. A watermark is a source-specific checkpoint; resets/replays can reread input without automatically undoing old output. Choose an output strategy safe for reprocessing.

### Practical example

```text
bookmark checkpoint=source batch 12
job writes batch 13 but fails before progress commit
retry reads 13 again -> destination must tolerate replay
```

**Expected result and reasoning:** Source progress and destination state are distinct concerns. Resetting a bookmark does not itself clean the target.

### Interview question

**Can bookmarks replace destination deduplication?**

No. They reduce repeated source processing under supported conditions. Use a sink with stable keys or deterministic partition publication and test crash recovery explicitly.

**Common mistake:** Deleting destination data broadly when resetting source progress.

**Try it yourself:** Design a targeted replay for one failed partition without modifying unrelated output.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

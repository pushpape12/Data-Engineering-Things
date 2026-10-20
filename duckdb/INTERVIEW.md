# DuckDB: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. CSV schemas
2. Analytical deduplication
3. Parquet export and inspection

## 1. CSV schemas

### Understand it

Local analytical engines can query files directly, but CSV has no native integer/date metadata. Inference is convenient for exploration; explicit schemas make repeatable pipelines safer when values change over time.

### Practical example

```sql
-- DuckDB from repository root:
SELECT COUNT(*) FROM read_csv('datasets/orders.csv',header=true);
```

**Expected result and reasoning:** Six rows are read. That is a physical event count, not the number of current orders.

### Interview question

**Why use DuckDB instead of pandas for a file analysis?**

SQL-based scans/joins/aggregates over files can simplify analytical work, including workloads beyond a simple in-memory DataFrame. Choose based on execution behavior, supported formats and team workflow; do not claim unlimited memory.

**Common mistake:** Assuming sampled type inference is a source contract.

**Try it yourself:** Add a nonnumeric amount and decide whether to fail or quarantine.

## 2. Analytical deduplication

### Understand it

A latest-state view must resolve versions before business aggregation. Canonical timestamp strings can sort correctly for this controlled fixture; general timestamps should be parsed with timezone/format policy.

### Practical example

```bash
duckdb < duckdb/orders.sql
```

**Expected result and reasoning:** Customer revenues are 101=450 and 102=250 after rejecting the negative amount and keeping one latest order version.

### Interview question

**How do you analyze duplicated event files without a permanent warehouse?**

Read them with explicit types, create a temporary ranked view, validate expected grain and aggregate the selected state. Retain source filenames/positions for debugging when needed.

**Common mistake:** Applying SUM to all events and mistaking updates for new sales.

**Try it yourself:** Compare current-state revenue to an event-count report and explain why both are valid but different.

## 3. Parquet export and inspection

### Understand it

A direct file query and an exported Parquet dataset can form a small local analytics workflow. Projection and predicate support depend on engine/file metadata. Record schema and controls when crossing formats.

### Practical example

```sql
-- Same DuckDB session after loading duckdb/orders.sql; create output/ first.
COPY current_orders TO 'output/current_orders.parquet' (FORMAT PARQUET);
SELECT COUNT(*),SUM(amount_cents) FROM read_parquet('output/current_orders.parquet');
```

**Expected result and reasoning:** Output should be 3 and 700. This optional export was not executed in this revision.

### Interview question

**What would you verify after conversion to Parquet?**

Row counts, key uniqueness, totals, column types, nulls and timestamp semantics. Compare a round-trip result rather than checking only that a file exists.

**Common mistake:** Assuming a successful write proves no type/precision changes occurred.

**Try it yourself:** Compare schema of the original CSV interpretation and exported Parquet.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

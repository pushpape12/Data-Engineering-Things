# File formats and data layout: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. CSV and JSON Lines
2. Parquet
3. Partitioning and small files

## 1. CSV and JSON Lines

### Understand it

CSV requires an external contract for delimiter, quoting, header and types. JSON Lines uses one JSON object per line and supports nested structure, but it does not itself enforce field types or schema compatibility. Escaped newlines differ from physical line breaks.

### Practical example

```json
{"order_id":1,"amount_cents":150}
{"order_id":2,"amount_cents":250}
```

**Expected result and reasoning:** Two physical lines represent two records; the amount total is 400. A pretty-printed multi-line JSON array is not this format.

### Interview question

**When choose JSON Lines instead of CSV?**

When nested/optional fields and incremental record parsing are useful, while accepting its verbosity and schema-validation needs. CSV is simple for flat exchanges; both need contracts and validation.

**Common mistake:** Assuming JSON implies stable types because values have syntax types.

**Try it yourself:** Represent an order with two items and specify the analytical grain after flattening.

## 2. Parquet

### Understand it

Parquet stores typed columnar data with row groups and metadata. Analytical engines can often read only selected columns and prune using available metadata. It is a physical file format, not a multi-file transaction protocol.

### Practical example

```python
# Optional: pandas with an installed Parquet engine.
import pandas as pd
frame = pd.DataFrame({'order_id':[1,2],'amount_cents':[150,250]})
frame.to_parquet('output/interview-orders.parquet',index=False)
read_back = pd.read_parquet('output/interview-orders.parquet',columns=['amount_cents'])
print(read_back['amount_cents'].sum())
```

**Expected result and reasoning:** After creating output/ and installing a compatible Parquet engine, the result is 400. This round-trip is unexecuted in this revision.

### Interview question

**Why is Parquet often faster than CSV for analytics?**

It preserves types and supports efficient column-oriented encoding, compression and metadata-assisted skipping in compatible engines. Benefits depend on query shape, file layout and reader behavior.

**Common mistake:** Claiming Parquet alone provides ACID updates across a directory.

**Try it yourself:** Compare a query reading two columns from a hundred-column CSV versus Parquet.

## 3. Partitioning and small files

### Understand it

Storage partitioning narrows file discovery for common predicates; files within partitions need sensible sizes. Excessively granular keys create many tiny objects, while overly broad partitions can scan too much. Compaction must preserve transactional reader semantics where applicable.

### Practical example

```text
daily data: 200 GB
layout A: order_date partitions with a manageable number of files
layout B: event_id partitions with one tiny file per event
```

**Expected result and reasoning:** Layout B increases metadata/listing/task overhead at high event cardinality. No single file-size number is optimal for every engine/workload.

### Interview question

**How do you solve the small-file problem?**

Find the cause, balance write parallelism, choose useful partition cardinality and compact using the table format/engine's supported procedure. Measure read/write impact and preserve active snapshots.

**Common mistake:** Manually deleting small files without updating a transactional table's metadata.

**Try it yourself:** Design a compaction schedule for continuously arriving hourly data.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

# Data engineering foundations: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. ETL versus ELT
2. Batch versus streaming
3. Grain and dimensional modeling
4. Idempotency and CDC

## 1. ETL versus ELT

### Understand it

ETL transforms before writing the destination; ELT lands data first and transforms using destination compute. Both still need validation, lineage and replay. Choose based on the sensitivity of raw fields, transformation size and destination capabilities rather than tool popularity.

### Practical example

```text
ETL: source CSV -> remove confidential columns -> warehouse
ELT: public order events -> raw table -> SQL staging -> revenue mart
```

**Expected result and reasoning:** The ETL path prevents confidential columns from reaching the warehouse. The ELT path preserves raw public events for rebuilding models.

### Interview question

**When would you choose ETL instead of ELT?**

Choose ETL when transformation or redaction must happen before landing, or the destination is unsuitable for the work. Choose ELT when governed raw retention and warehouse processing simplify rebuilds. Describe where rejected records go in either architecture.

**Common mistake:** Saying ELT eliminates data quality work.

**Try it yourself:** Describe how a customer email field changes each design.

## 2. Batch versus streaming

### Understand it

Batch processes a bounded input. Streaming maintains state over an unbounded sequence and must decide how event-time windows close. Arrival time and business event time differ; a late event can belong to an earlier reporting period.

### Practical example

```text
event_time=10:01, arrival_time=10:08
5-minute event-time window: [10:00,10:05)
arrival-time window: [10:05,10:10)
```

**Expected result and reasoning:** The same event belongs to different windows under the two time definitions. Late-event policy determines whether the earlier result is corrected.

### Interview question

**Does running every minute make a pipeline streaming?**

No. A scheduled bounded job is micro-batch. Discuss latency objectives, state, checkpoints, event time and late-data corrections. Some streaming engines internally use micro-batches, so scheduling frequency alone does not define the architecture.

**Common mistake:** Dropping late events without defining acceptable lateness.

**Try it yourself:** Design a daily correction job for events arriving two days late.

## 3. Grain and dimensional modeling

### Understand it

Declare what one row represents before choosing keys or joins. An order fact differs from an order-item fact. Dimensions add descriptive context. A slowly changing dimension can preserve historical attributes, but its temporal join must choose exactly one applicable version.

### Practical example

```text
order 10: total=1000 cents
items: (10,A,600), (10,B,400)
join order total to both items -> SUM(order_total)=2000
```

**Expected result and reasoning:** The join duplicates the order-level amount. Aggregate items at order grain or use item amounts at item grain.

### Interview question

**Why did a revenue total double after a join?**

Check key uniqueness and the grain of both sides. Count matched rows per key, inspect one-to-many relationships, and aggregate at a consistent grain before summing measures.

**Common mistake:** Using DISTINCT after the join to conceal an undefined grain.

**Try it yourself:** Model a customer dimension with a historical address change.

## 4. Idempotency and CDC

### Understand it

Idempotency means repeating the same logical operation leaves the same result. CDC adds operation type and source ordering to business keys. Upserts handle insert/update state; deletes require tombstones or deletion logic. Commit the output and checkpoint coherently.

### Practical example

```text
order 1 v1=100 -> order 1 v2=150 -> replay v1
unguarded upsert: 100
source-version guard: 150
```

**Expected result and reasoning:** The old replay must not regress state. Arrival order does not establish business order.

### Interview question

**How do you make an incremental load retry-safe?**

Use a stable business/event key, deterministic source version and an atomic destination write. Reprocess a known interval and guard against older versions. Track progress only after successful publication; explicitly define deletes and conflicting versions.

**Common mistake:** Calling a timestamp watermark alone an exactly-once guarantee.

**Try it yourself:** Add a tombstone v3 and explain why replay v2 must not recreate the row.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

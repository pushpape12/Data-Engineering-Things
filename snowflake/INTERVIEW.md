# Snowflake: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Architecture and compute
2. Stages, file formats and COPY
3. Deterministic MERGE
4. VARIANT and FLATTEN
5. Streams and tasks
6. Time Travel and cloning
7. Access control and cost
8. Micro-partitions and pruning
9. Result reuse versus warehouse cache

## 1. Architecture and compute

### Understand it

Snowflake separates stored data from warehouse compute and shared services. Separate workloads can use different warehouses over the same governed data. Scaling up gives a warehouse more compute; multi-cluster configurations primarily address concurrency. Neither replaces fixing inefficient SQL.

### Practical example

```sql
SELECT CURRENT_ROLE(),CURRENT_WAREHOUSE(),CURRENT_DATABASE(),CURRENT_SCHEMA();
SHOW WAREHOUSES;
```

**Expected result and reasoning:** Inspect your actual session and warehouse configuration; no fixed output is assumed. Run read-only in an authorized account.

### Interview question

**Scale up or scale out: which would you choose?**

For one resource-constrained query, inspect the profile and consider warehouse size. For queued concurrent queries, consider workload separation or supported concurrency features. Measure cost per completed workload, not only runtime.

**Common mistake:** Claiming multi-cluster automatically speeds one query.

**Try it yourself:** Explain a design that isolates ingestion from dashboard traffic.

## 2. Stages, file formats and COPY

### Understand it

A stage points to files, a file format defines parsing, and COPY loads a target. Internal stages are managed storage locations; external stages reference cloud storage with authorized integrations. Retrying a load requires considering file history and downstream duplicates.

### Practical example

```sql
-- After the snowflake lab format/stage exists and the CSV is uploaded:
LIST @de_lab_stage;
-- Prepare an empty raw_order_events table matching the CSV contract first.
-- COPY INTO raw_order_events FROM @de_lab_stage/orders.csv
-- FILE_FORMAT=(FORMAT_NAME=de_lab_csv) ON_ERROR=ABORT_STATEMENT;
```

**Expected result and reasoning:** LIST should display the uploaded file. The commented COPY template must be adapted to an existing scratch target and its five CSV fields.

### Interview question

**How would you investigate failed Snowflake loading?**

Check stage visibility, integration privileges, file format, column conversion and load history. Reproduce with a small authorized file and validation options where supported, then decide how to quarantine or retry.

**Common mistake:** Using FORCE to reload everything without assessing duplicate impact.

**Try it yourself:** Explain how a new schema field would affect positional CSV loading.

## 3. Deterministic MERGE

### Understand it

MERGE needs an unambiguous source match per target key. Deduplicate source versions and reject equal-version conflicting payloads upstream. Destination updates should apply only newer source versions, so late replays cannot roll back state.

### Practical example

```sql
-- After snowflake/examples.sql:
SELECT order_id,amount_cents FROM de_lab_orders ORDER BY order_id;
-- Source reduction pattern:
-- QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id
-- ORDER BY updated_at DESC,event_id DESC)=1
```

**Expected result and reasoning:** The lab returns 1=150,2=250,3=300. Replaying only its MERGE keeps the state unchanged.

### Interview question

**Why might a MERGE produce a nondeterministic update error?**

Multiple source rows may match one target row with conflicting actions/values. Define one source winner per business key or reject ambiguity before merging. Also check duplicate target keys; do not assume unenforced uniqueness constraints protect standard tables.

**Common mistake:** Suppressing nondeterminism instead of defining source order.

**Try it yourself:** Add a stale update for order 1 and explain the version guard.

## 4. VARIANT and FLATTEN

### Understand it

VARIANT stores semi-structured values. Paths navigate JSON; explicit casts produce analytical types. FLATTEN creates one row per selected array element, so aggregation must respect the resulting grain.

### Practical example

```sql
WITH d AS (SELECT PARSE_JSON('{"order_id":1,"items":[{"sku":"A","qty":2},{"sku":"B","qty":1}]}') p)
SELECT p:order_id::INT order_id,f.value:sku::STRING sku,f.value:qty::INT qty
FROM d,LATERAL FLATTEN(INPUT=>p:items) f;
```

**Expected result and reasoning:** Two rows: (1,A,2) and (1,B,1). Order-level revenue would be duplicated if summed across these rows.

### Interview question

**How do you query an array in a JSON column?**

Select the array path with FLATTEN, navigate each returned VALUE, cast fields explicitly and preserve parent identity. Define how empty/missing arrays should behave and whether OUTER is appropriate.

**Common mistake:** Summing parent-level measures after flattening without returning to parent grain.

**Try it yourself:** Add an empty items array and compare default versus OUTER behavior.

## 5. Streams and tasks

### Understand it

A stream exposes changes relative to an offset; a task schedules or triggers SQL. An ordinary SELECT does not consume a stream. Committed DML that consumes it advances progress. Standard streams represent updates differently from append-only insert streams.

### Practical example

```sql
-- During snowflake/streams-tasks.sql:
SELECT COUNT(*) FROM de_lab_append_stream;
INSERT INTO de_lab_append_sink SELECT order_id,amount_cents FROM de_lab_append_stream;
SELECT COUNT(*) FROM de_lab_append_stream;
```

**Expected result and reasoning:** For the lab's two inserts, count changes from 2 to 0 after committed consumption. The provided task remains suspended.

### Interview question

**Can two independent consumers share one stream offset?**

If they need independent progress, use separate streams. For coordinated writes from the same change set, use an explicit transaction and carefully controlled consumers. Monitor staleness and recovery windows.

**Common mistake:** Recreating a stream during routine retries and losing its prior offset.

**Try it yourself:** Describe recovery when a consumer falls beyond retained change history.

## 6. Time Travel and cloning

### Understand it

Time Travel queries retained historical data. A zero-copy clone creates an independent object initially referencing shared storage; later divergence changes storage use. Available history depends on retention and object characteristics. Neither implies an unlimited backup.

### Practical example

```sql
-- Templates for an authorized persistent table with available history:
-- SELECT * FROM orders AT(OFFSET => -60);
-- CREATE TABLE orders_debug CLONE orders;
-- SELECT COUNT(*) FROM orders_debug;
```

**Expected result and reasoning:** The clone initially reflects the selected source snapshot. These are templates rather than commands executed in this revision.

### Interview question

**Is cloning the same as copying every file?**

No. Existing storage can initially be shared through metadata. Objects can diverge after writes. Explain retention, permissions and cleanup; use an explicit backup/recovery strategy for requirements beyond retained history.

**Common mistake:** Promising historical recovery after required files/history have expired.

**Try it yourself:** Compare a short-lived debugging clone with a long-term backup requirement.

## 7. Access control and cost

### Understand it

A usable role needs the full access chain: relevant database/schema usage, object access and compute rights when required. Cost analysis includes warehouse activity, storage and separately billed services. Avoid broad privileges as a troubleshooting shortcut.

### Practical example

```sql
SELECT CURRENT_ROLE();
SHOW GRANTS;
SHOW WAREHOUSES;
```

**Expected result and reasoning:** Read your role's visible access and compute settings. Actual rows depend on the account.

### Interview question

**A user can see a table but cannot query it. What do you check?**

Confirm the active role and inherited grants, database/schema USAGE, table SELECT and warehouse USAGE/availability. Resolve the missing permission narrowly rather than granting administrator access.

**Common mistake:** Treating a resource monitor as a universal hard cap on all Snowflake spend.

**Try it yourself:** Design a reader role and separate ingestion role for one sandbox schema.

## 8. Micro-partitions and pruning

### Understand it

For standard analytical tables, Snowflake stores columnar micro-partitions and metadata that can skip irrelevant data. Clustering organization can influence pruning. A clustering key is not a B-tree index; maintenance has a cost.

### Practical example

```sql
-- Against a representative large table with order_ts:
-- SELECT SUM(amount_cents) FROM orders
-- WHERE order_ts >= '2026-10-01'::TIMESTAMP_NTZ
--   AND order_ts < '2026-10-02'::TIMESTAMP_NTZ;
```

**Expected result and reasoning:** Use Query Profile to compare scanned versus total partitions. A tiny fixture cannot meaningfully prove pruning efficiency.

### Interview question

**When would you add a clustering key?**

When repeated selective queries on a sufficiently large table show poor pruning and the expected workload benefit outweighs maintenance cost. Verify with profiles and representative predicates rather than adding keys to every table.

**Common mistake:** Assuming every selective predicate guarantees equal proportional scan reduction.

**Try it yourself:** Compare a broad date query and a narrow date query on the same realistic dataset.

## 9. Result reuse versus warehouse cache

### Understand it

Persisted query results and warehouse-local cached data are different mechanisms. Eligible result reuse can avoid recomputation; local data caching helps queries that still execute. Benchmark conditions must distinguish them.

### Practical example

```sql
ALTER SESSION SET USE_CACHED_RESULT=FALSE;
-- Run the query you are measuring and inspect its profile.
ALTER SESSION SET USE_CACHED_RESULT=TRUE;
```

**Expected result and reasoning:** The session setting disables persisted result reuse while false; it does not automatically clear the warehouse's data cache.

### Interview question

**Why is the second execution faster?**

It could be persisted results, warm warehouse data, compilation or other workload effects. Check the profile and control benchmark conditions before crediting a SQL rewrite.

**Common mistake:** Calling USE_CACHED_RESULT=FALSE a complete cold-cache benchmark.

**Try it yourself:** Write a benchmark plan that reports both warm and cold conditions.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

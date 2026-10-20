# PostgreSQL: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Constraints and keys
2. Version-aware upserts
3. Indexes and query plans

## 1. Constraints and keys

### Understand it

A primary key enforces identity and non-null uniqueness. Composite keys represent combined grain. Foreign keys check relationships under configured semantics; they do not define every business quality rule.

### Practical example

```sql
CREATE TEMP TABLE steps(run_id TEXT,step TEXT,status TEXT,PRIMARY KEY(run_id,step));
INSERT INTO steps VALUES('r1','extract','SUCCESS'),('r1','load','RUNNING');
SELECT COUNT(*) FROM steps;
```

**Expected result and reasoning:** Output is 2 because step is part of identity. Inserting another ('r1','load',...) without conflict handling fails.

### Interview question

**Why does a step-status table need a composite key?**

One run contains multiple steps. run_id alone cannot distinguish them; use a stable step identifier with run_id. Decide whether retries overwrite current status or create an attempt-history table.

**Common mistake:** Using an ORM model with no mapped primary key and expecting reliable updates.

**Try it yourself:** Add attempt history without losing a unique current-state lookup.

## 2. Version-aware upserts

### Understand it

ON CONFLICT relies on an applicable unique key. Update conditions protect against stale writes, but timestamp ties and concurrent workflows still need a defined source-order contract. Use transactions for related changes.

### Practical example

```sql
-- Inside the transaction from postgresql/upsert.sql, before ROLLBACK:
INSERT INTO de_lab_orders VALUES(1,90,'2026-10-01T09:00:00Z')
ON CONFLICT(order_id) DO UPDATE SET amount_cents=EXCLUDED.amount_cents
WHERE EXCLUDED.updated_at>de_lab_orders.updated_at;
SELECT amount_cents FROM de_lab_orders WHERE order_id=1;
```

**Expected result and reasoning:** The amount stays 150 because 09:00 is older than the existing source version. The example uses timestamp order without an equal-time tie-breaker.

### Interview question

**How does an upsert differ from SELECT-then-INSERT?**

A constraint-backed upsert lets the database coordinate conflicts atomically. Separate existence checking can race with another writer. You still need appropriate transaction isolation and a business conflict policy.

**Common mistake:** Catching every unique violation and returning success without validating which operation won.

**Try it yourself:** Extend the predicate to use a monotonic source sequence.

## 3. Indexes and query plans

### Understand it

An index can speed selective lookups at the cost of storage and write maintenance. Composite index column order matters. EXPLAIN shows an estimated plan; EXPLAIN ANALYZE runs the statement and collects actual execution measurements.

### Practical example

```sql
-- In the scratch transaction:
EXPLAIN SELECT * FROM de_lab_orders WHERE order_id=1;
```

**Expected result and reasoning:** For two rows, a sequential scan may be rational. Use representative statistics/cardinality before drawing performance conclusions.

### Interview question

**Why didn't PostgreSQL choose my index?**

The planner may expect a broad scan, estimates may be stale, an expression/type may not match the index, or the table may be tiny. Compare estimated/actual rows and update statistics through an appropriate operational process.

**Common mistake:** Running EXPLAIN ANALYZE on a modifying production statement assuming it is read-only.

**Try it yourself:** Explain a composite (customer_id,updated_at) index for per-customer time-range queries.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

# dbt: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. ref and model dependencies
2. Seeds and data tests
3. Incremental model design
4. Snapshots and historical attributes

## 1. ref and model dependencies

### Understand it

ref resolves a model relation and declares dependency lineage. Staging standardizes input; downstream marts own business definitions. A materialization decides whether the relation is a view/table/incremental structure, not whether the SQL is semantically correct.

### Practical example

```sql
select customer_id,sum(amount_cents) as revenue_cents
from {{ ref('stg_orders') }}
group by customer_id
```

**Expected result and reasoning:** The bundled seed/model lab produces customer 101=450 and 102=250 after its latest-state staging logic.

### Interview question

**What is ref doing besides generating a table name?**

It records dependencies so dbt can order builds, select related models and generate lineage. It also resolves environment-aware relation naming through the adapter/project configuration.

**Common mistake:** Hardcoding a development schema in every model instead of dependency references.

**Try it yourself:** Explain how a staging schema change should be tested against downstream marts.

## 2. Seeds and data tests

### Understand it

Seeds are versioned small reference/test datasets. Data tests query whether expected properties hold, such as uniqueness or non-nullness. Passing structural tests does not prove metric correctness or source completeness.

### Practical example

```yaml
version: 2
models:
  - name: stg_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
```

**Expected result and reasoning:** The example rejects duplicate/null order IDs in stg_orders when executed in the configured dbt project. It does not check the expected 700-cent revenue by itself.

### Interview question

**What would you test beyond unique and not_null?**

Reconciliation totals, relationships, accepted business values, source freshness and domain-specific rules. Make failures actionable and choose severity based on the publication contract.

**Common mistake:** Assuming zero duplicates means no source records are missing.

**Try it yourself:** Design a singular test for a negative amount or mismatch against a trusted control total.

## 3. Incremental model design

### Understand it

Incremental models process selected changes and reconcile them with existing output using an adapter-supported strategy. A unique_key identifies rows for supported matching behavior; it is not a universal database constraint. Late arrivals, deletes and schema changes need explicit policies.

### Practical example

```text
source updates read with overlap -> deduplicate versions
merge by order_id with source-order condition
reconcile -> record source progress
```

**Expected result and reasoning:** Repeated input must not add a second current order. A timestamp-only filter can miss equal-timestamp or late updates.

### Interview question

**Why can an incremental model miss data?**

A filter may assume arrival order, source timestamps may be nonmonotonic or ties may be excluded; hard deletes may be absent from the feed. Add a bounded overlap with guarded merges or use source CDC sequences when available.

**Common mistake:** Declaring unique_key and assuming it automatically rejects all duplicate source rows.

**Try it yourself:** Explain when a full refresh is appropriate and how to control its downstream impact.

## 4. Snapshots and historical attributes

### Understand it

dbt snapshots preserve observed changes in a mutable source using an SCD-style history. They cannot recover changes that occurred and disappeared between observations unless the source exposes them. Select an appropriate unique key and change detection strategy.

### Practical example

```text
09:00 source city=Delhi -> snapshot observes Delhi
10:00 source city=Hyderabad -> snapshot observes Hyderabad
history: Delhi valid until next observed version; Hyderabad current
```

**Expected result and reasoning:** History records observed versions. An unobserved intermediate city cannot be reconstructed from these two snapshots.

### Interview question

**Snapshot or incremental model: which should store customer history?**

Use snapshots when preserving observed source attribute changes is the goal. Use incremental models for efficient transformation/publication of selected changes. Explain source truth, temporal semantics and delete handling rather than treating them as interchangeable.

**Common mistake:** Claiming a nightly snapshot is a complete CDC audit trail.

**Try it yourself:** Describe what happens if a customer changes twice between nightly snapshots.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

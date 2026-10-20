# Databricks and Delta Lake: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Bronze, silver and gold
2. Delta MERGE
3. History and recovery
4. Governance and jobs

## 1. Bronze, silver and gold

### Understand it

Bronze preserves source evidence, silver normalizes validated records, and gold represents business-ready data. Define each layer's grain and ownership. Layers need not mean three redundant full copies; choose physical materialization based on replay, cost and access needs.

### Practical example

```text
bronze: order versions [100,150] plus duplicates
silver: order 1 current amount=150
gold: customer 101 current revenue=450
```

**Expected result and reasoning:** Raw event counts and current order counts differ. A dashboard must not aggregate all versions as fresh sales.

### Interview question

**What belongs in the silver layer?**

Validated types, normalized keys, deduplication and explicit source-order handling. Keep business-wide metric definitions in governed downstream models and preserve rejects for diagnosis.

**Common mistake:** Calling any folder named silver a validated dataset.

**Try it yourself:** Choose where to store invalid events and who can view them.

## 2. Delta MERGE

### Understand it

Delta combines table-level transaction metadata with data files. Upserts still need deterministic source keys, conflict policy and stale-version guards. ACID storage does not infer business identity from duplicate input.

### Practical example

```sql
-- Run databricks/merge.sql first in its scratch schema:
SELECT order_id,amount_cents FROM de_lab_orders ORDER BY order_id;
DESCRIBE HISTORY de_lab_orders;
```

**Expected result and reasoning:** Rows are (1,150),(2,250). Replay only MERGE, not CREATE/initial INSERT, to test idempotency.

### Interview question

**Does MERGE automatically remove duplicate source records?**

No. Reduce ambiguous source matches before MERGE, enforce the intended target grain through pipeline checks and apply only newer versions. Equal-version conflicts need a deliberate policy.

**Common mistake:** Assuming ACID means exactly one row per business entity without validation.

**Try it yourself:** Add two updates for order 1 in one source batch and select a deterministic winner.

## 3. History and recovery

### Understand it

Delta history records commits; historical reads need the relevant metadata and data files. Maintenance retention is part of recovery policy. Optimizations and compaction change physical files, while a logical snapshot still identifies a table version.

### Practical example

```sql
-- In the same scratch lab:
DESCRIBE HISTORY de_lab_orders;
SELECT * FROM de_lab_orders VERSION AS OF 0;
```

**Expected result and reasoning:** Version 0 from the initial CREATE is empty in this lab; subsequent history identifies writes. Do not assume a fixed latest version in shared environments.

### Interview question

**Why can time travel fail even if a version number is known?**

Required logs or data files may no longer exist, or permissions/runtime compatibility may prevent access. Validate retention and recovery requirements before maintenance.

**Common mistake:** Running VACUUM with aggressive retention as a routine troubleshooting step.

**Try it yourself:** Design a retention policy for a seven-day rollback objective.

## 4. Governance and jobs

### Understand it

Catalog/schema privileges, compute identity and storage access must align. Parameterized jobs make source interval, target and checkpoint visible. Keep production secrets outside notebooks and avoid job designs tied to one engineer's interactive session.

### Practical example

```text
job params: run_date=2026-10-01, target=sandbox.orders
job identity: limited service principal
artifacts: source manifest + commit/run metadata
```

**Expected result and reasoning:** A rerun uses the same logical interval with an identifiable version, rather than today's date or an interactive user's default schema.

### Interview question

**How would you promote a notebook pipeline to production?**

Extract reusable transformations, parameterize paths, establish a job identity, test contracts/replay, add observability, then deploy versioned artifacts through CI. Select a compatible runtime and governance policy.

**Common mistake:** Hardcoding a personal token in notebook configuration.

**Try it yourself:** Explain how dev and prod should differ in configuration but share tested transformation code.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

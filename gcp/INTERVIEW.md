# Google Cloud data engineering: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. GCS, Pub/Sub and Dataflow
2. BigQuery partitioning and clustering
3. Schema and load jobs

## 1. GCS, Pub/Sub and Dataflow

### Understand it

GCS is object storage, Pub/Sub transports messages and Dataflow executes Beam pipelines. Pick delivery identity, event time and sink guarantees independently; a managed service does not remove the need for end-to-end correctness checks.

### Practical example

```text
Pub/Sub order event -> Dataflow validation -> BigQuery staging
staging -> one latest version/order -> business aggregate
```

**Expected result and reasoning:** Retries can duplicate event deliveries even if the final business table is kept unique by its publication design.

### Interview question

**When choose Dataflow rather than a scheduled warehouse query?**

Choose a streaming processing engine when latency, stateful event-time work or source/sink processing justify it. Use scheduled SQL for suitable bounded warehouse transformations with simpler operational requirements.

**Common mistake:** Treating message delivery guarantees as identical to final database business semantics.

**Try it yourself:** Design an event-time correction for a message delivered an hour late.

## 2. BigQuery partitioning and clustering

### Understand it

Partitioning separates data by supported partition expressions; clustering organizes blocks within partitions/table storage around selected fields. Partition filters and selective clustered predicates can reduce reads; physical behavior should be measured.

### Practical example

```sql
-- After adapting/running gcp/bigquery.sql:
SELECT customer_id,SUM(amount_cents)
FROM `YOUR_PROJECT.sandbox.de_lab_orders`
WHERE order_date=DATE '2026-10-01'
GROUP BY customer_id;
```

**Expected result and reasoning:** The two-row GCP lab returns 101=150 and 102=250, unlike the larger shared fixture. Use dry-run estimates on realistic data.

### Interview question

**Partitioning or clustering: which is better?**

They are complementary. Choose a partition key aligned with common bounded filters and clustering fields that benefit selective access within those partitions, while considering table size and query patterns.

**Common mistake:** Claiming clustering guarantees a fixed output order or exact scan size.

**Try it yourself:** Explain how require_partition_filter prevents accidental broad queries.

## 3. Schema and load jobs

### Understand it

Schema contracts prevent accidental type inference drift. Job identity, output write mode and staging design determine retry behavior. Load raw data before validated merge when input can contain repeated source versions.

### Practical example

```text
stable load identity -> staging table -> validate
latest per business key -> MERGE -> reconciliation -> checkpoint
```

**Expected result and reasoning:** Rerunning should not blindly append the same logical batch to the final table. An explicit staging/publication boundary makes recovery easier.

### Interview question

**How would you handle an API timeout on a load job?**

Check the known job identity/status before resubmitting. If the prior job succeeded, continue verification; if uncertain, preserve idempotent load and destination semantics rather than generating duplicates.

**Common mistake:** Assuming a timeout proves the backend failed.

**Try it yourself:** Describe adding a nullable source field versus changing a numeric field to free text.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

# Apache Airflow: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. DAGs and TaskFlow
2. Retries and idempotency
3. Scheduling and logical intervals
4. XComs and connections

## 1. DAGs and TaskFlow

### Understand it

Airflow parses DAG code to construct a dependency graph; tasks run later on configured execution infrastructure. A TaskFlow call creates task dependencies. Expensive top-level work slows parsing and can fail before any task instance starts.

### Practical example

```python
# Pattern used by airflow/orders_dag.py:
report(validate(extract_manifest()))
```

**Expected result and reasoning:** The dependency graph is extract_manifest -> validate -> report. The small fixture ultimately reports two rows totalling 400 cents.

### Interview question

**Why should database calls stay out of DAG top-level code?**

The scheduler repeatedly parses files. Top-level calls can slow or destabilize scheduling and produce uncontrolled side effects. Put runtime I/O inside tasks and use configured connections.

**Common mistake:** Thinking a decorated function executes its business logic during DAG construction.

**Try it yourself:** Explain where DAG parameters are read and where source extraction executes.

## 2. Retries and idempotency

### Understand it

An orchestration retry can repeat already committed side effects. The orchestrator records task state separately from an external data transaction. Use stable run intervals and idempotent destinations rather than relying on retries to clean output.

### Practical example

```text
task writes orders -> worker dies before success record
airflow retries task -> same batch upsert -> unchanged orders
```

**Expected result and reasoning:** The task may execute twice even though the intended dataset should be published once.

### Interview question

**How do retries and backfills differ?**

A retry repeats a failed task attempt for a logical run. A backfill creates/processes historical logical intervals. Both need deterministic inputs, conflict control and safe destination writes.

**Common mistake:** Using a new output timestamp on each retry and appending duplicates.

**Try it yourself:** Decide which errors should fail immediately rather than retry.

## 3. Scheduling and logical intervals

### Understand it

The logical run relates to a data interval, not simply the current wall clock. For a daily timetable, processing typically follows interval completion. Catchup creates missing scheduled intervals according to configuration; manual backfills are a separate operational choice.

### Practical example

```text
daily interval: [2026-10-01 00:00Z,2026-10-02 00:00Z)
extract lower inclusive, upper exclusive
an event at 2026-10-02 00:00Z belongs to the next interval
```

**Expected result and reasoning:** Half-open boundaries prevent adjacent runs from both claiming the boundary event. Timezone/DST and timetable choices must be explicit.

### Interview question

**Why not use datetime.now() to select a daily partition?**

A retry tomorrow or a historical backfill would target the wrong date. Use the intended data interval and a separately defined overlap policy for late records.

**Common mistake:** Equating catchup=False with making every task replay-safe.

**Try it yourself:** Explain a daylight-saving change for a business-local daily schedule.

## 4. XComs and connections

### Understand it

XCom is for exchanging small task results/metadata; large datasets should reside in storage. Workers may execute on different hosts, so a local file path is not a shared handoff unless the deployment explicitly provides shared storage.

### Practical example

```json
{"uri":"s3://YOUR_BUCKET/orders/batch-001.parquet","rows":3,"checksum":"example-digest","schema_version":1}
```

**Expected result and reasoning:** This is a metadata manifest; the data is not serialized into the scheduler database. The URI and digest are illustrative.

### Interview question

**How do two tasks share a 100 GB result?**

Write it to durable storage, return a manifest/URI and checksum, and give the next task authorized read access. Configure secrets through supported connections/backends rather than returning them in XCom.

**Common mistake:** Passing a DataFrame or access token through XCom.

**Try it yourself:** Specify how task B verifies it is reading the completed output rather than a partial file.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

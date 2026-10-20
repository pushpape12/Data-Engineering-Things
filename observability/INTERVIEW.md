# Pipeline observability: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Structured run metrics
2. Freshness and SLAs
3. Actionable alerts

## 1. Structured run metrics

### Understand it

A useful run record connects logical interval, code/config version, source coordinates, destination and counts. Metrics must distinguish events from entities; traces/logs supply detail without introducing unbounded high-cardinality metric labels.

### Practical example

```json
{"job":"orders_daily","run_id":"demo","input_events":6,"rejected_events":1,"current_orders":3,"total_cents":700}
```

**Expected result and reasoning:** The count difference is expected because valid events include historical and repeated deliveries. Each metric's definition must be documented.

### Interview question

**What would you monitor beyond job duration?**

Freshness, source/target completeness, reject rate, duplicate/conflict rate, backlog, resource use and successful publication. Correlate run IDs across orchestration and storage.

**Common mistake:** Using every order ID as a metric label, creating cardinality explosion.

**Try it yourself:** Define which fields belong in aggregate metrics and which belong in diagnostic logs.

## 2. Freshness and SLAs

### Understand it

A pipeline can run successfully while repeatedly publishing stale source data. Distinguish job runtime, ingestion delay, event-time delay and consumer availability. Backfills need labels so historical business times do not trigger false live alerts.

### Practical example

```text
source event_time=10:00
arrived=10:05
curated published=10:07
ingest delay=5m; publish-after-arrival=2m; end-to-end=7m
```

**Expected result and reasoning:** Three latency measures reveal different bottlenecks. An empty source interval can legitimately produce no new event timestamp.

### Interview question

**The DAG is green but the dashboard is stale. What next?**

Check the actual source high watermark, selected interval, output commit/partition and consumer refresh. Determine whether the bottleneck is source arrival, transformation, publication or downstream caching.

**Common mistake:** Alerting only on process exit and ignoring dataset freshness.

**Try it yourself:** Design an alert for a partition expected by 07:00 local time.

## 3. Actionable alerts

### Understand it

Alerts should identify a breached objective, impacted dataset, owner and next action. Deduplicate related failures and distinguish transient retries from sustained publication failures. A runbook needs recovery steps and replay boundaries.

### Practical example

```text
alert: orders partition 2026-10-01 missing after deadline
check: source manifest, last successful watermark, rejects, destination commit
recover: replay only affected interval with guarded writes
verify: grain + totals + consumer availability
```

**Expected result and reasoning:** The runbook moves from diagnosis to a bounded, verifiable recovery rather than blindly restarting every job.

### Interview question

**How do you reduce alert fatigue?**

Prioritize consumer-impacting symptoms, use agreed thresholds and sustained windows, group dependent alerts and keep routing/runbooks current. Preserve diagnostics even when suppressing duplicate notifications.

**Common mistake:** Silencing all retry warnings without a final failed-run alert.

**Try it yourself:** Describe recovery if only gold publication failed after silver succeeded.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

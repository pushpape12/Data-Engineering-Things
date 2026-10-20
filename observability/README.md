# Pipeline observability

Track whether correct data arrived on time, not only whether a process exited successfully.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Worked metric and runbook designs, with a query runnable against output/orders.db. No telemetry backend is installed.

## Topics with worked examples

### Structured run metrics

Emit stable fields for job/run IDs, source interval, counts and duration. Do not label customer/event IDs as unbounded metric dimensions.

```json
{"job":"orders_daily","run_id":"demo-2026-10-01","input_rows":6,"rejected_rows":1,"output_rows":3,"total_cents":700}
```

**Check:** These fixture counts support reconciliation; production metrics should distinguish input events from output state.

### Freshness and SLAs

Measure arrival lag and business event lag separately. An old source event timestamp may be legitimate during a backfill.

```sql
SELECT MAX(updated_at) AS latest_source_timestamp FROM orders;
```

**Check:** For the fixture: 2026-10-01T10:03:00Z. Do not treat fixed historical sample data as a live outage.

### Actionable alerts

Alert on a sustained breach with an owner and recovery step. Avoid firing for every retry if the pipeline recovers within its objective.

```text
Condition: curated partition absent 30 minutes after expected delivery
Owner: data platform on-call
Action: inspect source watermark, rejects and last successful publish
Recovery: replay the affected interval with idempotent writes
```

**Check:** Runbooks need source coordinates and durable run status, not only a stack trace.

## Official references

- https://opentelemetry.io/docs/concepts/observability-primer/

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

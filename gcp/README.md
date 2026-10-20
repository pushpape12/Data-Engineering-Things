# Google Cloud data engineering

Combine GCS landing data, BigQuery warehouse models and orchestration with source-aware replay.

[Back to repository index](../README.md)

## Prerequisites and lab

Run `bigquery.sql` only after replacing the project and creating a sandbox dataset. Needs BigQuery job/table permissions and can incur charges; not executed here.

## Topics with worked examples

### GCS, Pub/Sub and Dataflow

GCS holds objects, Pub/Sub transports events, and Dataflow runs Apache Beam pipelines. Delivery and processing guarantees depend on the configured pipeline and sink.

```text
GCS batch files -> BigQuery staging -> curated tables
Pub/Sub events -> Dataflow validation -> idempotent destination
```

**Check:** Define event identity before claiming exactly-once business results.

### BigQuery partitioning and clustering

Partition on a useful time/key boundary and cluster on selective filter keys. Require a partition filter to reduce accidental broad scans.

```sql
SELECT * FROM `YOUR_PROJECT.sandbox.de_lab_orders` WHERE order_date=DATE '2026-10-01';
```

**Check:** After bigquery.sql, two rows. Use dry-run estimates before executing large queries.

### Schema and load jobs

Specify schemas for stable ingestion, use stable job IDs where appropriate, and choose explicit append/truncate behavior.

```text
load raw -> validate contract -> deduplicate source keys -> MERGE curated -> commit watermark
```

**Check:** Never truncate the destination as an accidental retry strategy.

## Official references

- https://docs.cloud.google.com/bigquery/docs/partitioned-tables
- https://cloud.google.com/dataflow/docs/overview

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

# AWS data engineering

Compose object storage, catalog, compute and query services around an explicit data contract.

[Back to repository index](../README.md)

## Prerequisites and lab

Cloud templates only. Requires AWS CLI, an authorized sandbox role, appropriate region and existing resources. Queries and jobs can incur charges; this folder provisions nothing.

## Topics with worked examples

### S3 layout and partition pruning

Keep immutable landing events separate from curated outputs. Prefixes are object key conventions, not filesystem directories.

```text
s3://YOUR_BUCKET/raw/orders/ingest_date=2026-10-01/part-0001.jsonl
s3://YOUR_BUCKET/curated/orders/order_date=2026-10-01/part-0001.parquet
```

**Check:** A business date partition and an ingest date partition answer different questions.

### Glue catalog, Glue jobs and EMR

The catalog stores metadata; a Glue job executes transformations. EMR Serverless runs configured Spark/Hive applications. Select runtime-compatible dependencies and IAM roles.

```bash
aws glue get-database --name YOUR_SANDBOX_DATABASE
aws emr-serverless get-application --application-id YOUR_APPLICATION_ID
```

**Check:** Read-only templates: replace placeholders, authenticate with an approved role, and check region.

### Athena and cost-aware SQL

Partition filters reduce scanned data when the layout/catalog support pruning. Select only needed columns and inspect bytes scanned.

```sql
SELECT customer_id,SUM(amount_cents) FROM curated_orders WHERE order_date=DATE '2026-10-01' GROUP BY customer_id;
```

**Check:** Requires an existing table and configured results location; compare scanned bytes, not just query duration.

### Lambda and duplicate delivery

An S3-triggered Lambda may see repeated deliveries. Deduplicate against a durable event/object-version key and make sink writes idempotent.

```text
receive event -> claim object version -> validate -> write/upsert -> mark committed
crash after write -> replay -> sink idempotency prevents duplicate logical rows
```

**Check:** A marker alone is insufficient if the sink write and marker cannot commit atomically.

## Official references

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
- https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html
- https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/what-is-emr-serverless.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

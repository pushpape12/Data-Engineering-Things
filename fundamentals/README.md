# Data engineering foundations

Design pipelines around explicit grain, source ordering, data contracts and recoverability.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Start with [sample data](../datasets/README.md), then run the [Python lab](../python/README.md).

## Topics with worked examples

### ETL versus ELT

ETL validates/transforms before loading; ELT loads raw data then transforms in the destination. Choose based on privacy, compute location and replay requirements.

```text
CSV -> Python validation -> SQLite  (ETL)
Object storage -> raw warehouse table -> SQL models  (ELT)
```

**Check:** The local Python project is ETL; the Snowflake lab demonstrates destination SQL.

### Batch versus streaming

Batch bounds a dataset; streaming continually processes events. A five-minute schedule is micro-batch, not automatically low-latency streaming.

```text
10:00 batch: source versions through 09:59
10:05 batch: replay overlap plus newly arrived versions
```

**Check:** Define inclusion boundaries and late-data handling explicitly.

### Grain and dimensional modeling

A fact row represents one business measurement. Current order state and order events have different grains.

```sql
SELECT order_id,COUNT(*) FROM current_orders GROUP BY order_id HAVING COUNT(*)>1;
```

**Check:** Zero rows proves the intended one-row-per-order grain for this fixture.

### Idempotency and CDC

A retry must not create a second logical result. Store source versions; do not use arrival time to overwrite newer source state. Deletes need tombstones and retention policies beyond this insert/update lab.

```bash
python python/etl.py
python python/etl.py
```

**Check:** Both executions keep three orders and 700 cents, despite duplicates.

## Official references

- https://www.postgresql.org/docs/current/tutorial.html
- https://docs.python.org/3/library/sqlite3.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

# Apache Iceberg and open table formats

Distinguish a columnar file from a transactional table whose metadata manages snapshots and schema changes.

[Back to repository index](../README.md)

## Prerequisites and lab

Spark SQL templates only; configure Iceberg extensions/catalog and matching Spark/Scala artifacts using the official docs. Not executed here.

## Topics with worked examples

### Parquet versus Iceberg

Parquet encodes individual files. Iceberg adds table metadata, snapshots and partition evolution across a file collection.

```text
Parquet file: column chunks + row groups
Iceberg table: catalog pointer -> metadata -> snapshot -> manifests -> data/delete files
```

**Check:** Listing a directory is not equivalent to reading a consistent Iceberg snapshot.

### Catalog and partition transforms

Configure a compatible Spark/Iceberg catalog and runtime dependency before using SQL. Hidden partition transforms avoid manual derived partition columns.

```sql
CREATE TABLE local.learning.orders (
 order_id BIGINT, amount_cents BIGINT, event_time TIMESTAMP
) USING iceberg PARTITIONED BY (days(event_time));
INSERT INTO local.learning.orders VALUES(1,150,TIMESTAMP '2026-10-01 10:00:00');
SELECT * FROM local.learning.orders;
```

**Check:** Requires a preconfigured local catalog and learning namespace; one row after insert.

### Snapshots, maintenance and recovery

Inspect snapshots before expiring metadata or deleting orphan files. Cleanup can permanently remove historical data needed by readers.

```sql
SELECT committed_at,snapshot_id FROM local.learning.orders.snapshots;
```

**Check:** Observe commit metadata. No destructive maintenance command is executed in this guide.

## Official references

- https://iceberg.apache.org/docs/latest/spark-writes/
- https://iceberg.apache.org/spec/

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

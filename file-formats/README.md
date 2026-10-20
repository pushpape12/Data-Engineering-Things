# File formats and data layout

Choose serialization and physical layout based on access patterns, schema stability and interoperability.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Illustrative formats and an optional pandas/pyarrow round-trip. No Parquet engine is required for the standard-library project.

## Topics with worked examples

### CSV and JSON Lines

CSV needs an explicit delimiter/header/type contract. JSON Lines supports one object per line but still needs schema validation.

```json
{"order_id":1,"amount_cents":150,"updated_at":"2026-10-01T10:02:00Z"}
```

**Check:** One JSON object is one record; do not concatenate pretty-printed JSON and call it JSON Lines.

### Parquet

Parquet is columnar and useful for projection/filter-heavy analytics. Compression and row-group layout affect scan efficiency.

```python
# Requires pandas and a Parquet engine such as pyarrow; optional snippet.
current.to_parquet("output/orders.parquet",index=False)
read_back = pd.read_parquet("output/orders.parquet",columns=["order_id","amount_cents"])
```

**Check:** Use current from pandas/transform.py; expected three rows. Parquet execution is not validated here.

### Partitioning and small files

Choose a partition key that supports common filters without creating millions of tiny directories/objects. Partitioning by a unique event ID is usually a poor fit.

```text
Good candidate: orders/order_date=2026-10-01/part-000.parquet
Poor candidate at high cardinality: orders/event_id=e123/file.parquet
```

**Check:** Measure real file sizes and scans before setting compaction thresholds.

## Official references

- https://parquet.apache.org/docs/
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

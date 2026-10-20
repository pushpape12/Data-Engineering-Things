# DuckDB

Run analytical SQL locally over files without operating a database server.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Optional DuckDB CLI lab, not executed here. Run from repository root. The bundled SQL uses temporary views and creates no persistent database.

## Topics with worked examples

### CSV schemas

Explicit types prevent small samples from determining the wrong production contract.

```sql
SELECT COUNT(*) FROM read_csv('datasets/orders.csv',header=true);
```

**Check:** Six input events, including duplicates and a rejected negative amount.

### Analytical deduplication

Use a window to resolve source versions before business aggregation.

```bash
duckdb < duckdb/orders.sql
```

**Check:** The two customer totals are 450 and 250 cents.

### Parquet export and inspection

Columnar outputs can be inspected without importing them into a server. Preserve timestamp and money types deliberately.

```sql
COPY current_orders TO 'output/current_orders.parquet' (FORMAT PARQUET);
SELECT COUNT(*) FROM read_parquet('output/current_orders.parquet');
```

**Check:** Create output/ first; three exported rows after running orders.sql in the same session.

## Official references

- https://duckdb.org/docs/stable/data/csv/overview
- https://duckdb.org/docs/stable/data/parquet/overview

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

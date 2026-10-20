# dbt

Express warehouse transformations as versioned models with dependencies and data assertions.

[Back to repository index](../README.md)

## Prerequisites and lab

Optional local lab: in a dedicated environment install compatible `dbt-core` and `dbt-duckdb`. From `dbt/`, copy `profiles.yml.example` to `profiles.yml`, create `output/`, and run the commands below. Do not commit real profiles with secrets.

## Topics with worked examples

### ref and model dependencies

ref resolves models and records lineage. Keep staging cleanup separate from business aggregation.

```sql
select customer_id,sum(amount_cents) from {{ ref('stg_orders') }} group by customer_id
```

**Check:** customer_revenue returns 101=450 and 102=250.

### Seeds and data tests

Seeds suit small static fixtures, not large production ingest. Unique/not-null checks validate the final grain.

```bash
dbt seed --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
```

**Check:** The local DuckDB adapter lab should pass all declared tests; it is not executed in this environment.

### Incremental model design

An incremental model needs adapter-supported merge strategy, a unique key, deletion rules and a late-data policy. This project deliberately uses full views first.

```jinja
{# Design sketch, not a bundled executable model: #}
{{ config(materialized='incremental', unique_key='order_id') }}
-- Read changed versions plus overlap; deduplicate before adapter-specific MERGE.
```

**Check:** Do not add a naive max(timestamp) filter that loses late arrivals or deletes.

## Official references

- https://docs.getdbt.com/docs/build/incremental-models
- https://docs.getdbt.com/docs/build/data-tests

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

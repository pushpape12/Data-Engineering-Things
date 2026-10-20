# Snowflake

Practice warehouse SQL, loading, semi-structured data, incremental state and operational controls.

[Back to repository index](../README.md)

## Prerequisites and lab

Use a Snowflake sandbox with an existing warehouse. Execute `examples.sql` interactively. `streams-tasks.sql` needs extra privileges and a warehouse substitution; it does not resume the task. Cloud SQL has not been executed here.

## Topics with worked examples

### Architecture and compute

Storage and virtual warehouses are separate concerns. An existing small warehouse is enough for the lab; inspect auto-suspend instead of provisioning always-on compute.

```sql
SHOW WAREHOUSES;
SELECT CURRENT_DATABASE(),CURRENT_SCHEMA(),CURRENT_WAREHOUSE();
```

**Check:** Confirm a sandbox context before running either SQL file.

### Stages, file formats and COPY

A stage locates files; a file format defines parsing. The sample CSV has a header and five fields. Load into a raw table whose columns match the dataset contract.

```sql
CREATE FILE FORMAT de_lab_csv TYPE=CSV SKIP_HEADER=1;
CREATE STAGE de_lab_stage FILE_FORMAT=de_lab_csv;
-- Upload datasets/orders.csv into this internal stage using Snowsight or SnowSQL.
-- With a raw table matching the five CSV columns:
-- COPY INTO raw_order_events FROM @de_lab_stage/orders.csv ON_ERROR=ABORT_STATEMENT;
```

**Check:** Validate loaded/rejected row counts; COPY is a template until a raw table and upload exist.

### Deterministic MERGE

Reduce source rows to one per key before merging. Guard updates with source versions; this lab assumes conflicting equal versions have already been rejected.

```sql
SELECT order_id,amount_cents FROM de_lab_orders ORDER BY order_id;
```

**Check:** After examples.sql: 1=150, 2=250, 3=300. Rerunning MERGE leaves those values.

### VARIANT and FLATTEN

Keep raw JSON and flatten only the required array. Flattening multiple arrays can multiply rows.

```sql
WITH d AS (SELECT PARSE_JSON('{"items":[{"qty":2}]}') p)
SELECT f.value:qty::INT qty FROM d,LATERAL FLATTEN(INPUT=>p:items) f;
```

**Check:** One row with qty=2.

### Streams and tasks

A stream tracks changes relative to an offset. A SELECT does not consume it; committed DML consumption does. The separate lab uses append-only inserts, not update/delete CDC.

```sql
SELECT COUNT(*) FROM de_lab_append_stream;
```

**Check:** Count becomes zero after the INSERT into the sink. A task is included but remains suspended.

### Time Travel and cloning

Retention and object type determine historical availability. A clone shares existing storage initially; later changes can add storage.

```sql
-- Against an authorized persistent table with sufficient retention:
-- SELECT * FROM orders AT(OFFSET => -60);
-- CREATE TABLE orders_debug CLONE orders;
```

**Check:** These are opt-in templates; a clone is not an independent long-term backup.

### Access control and cost

Grant only needed object privileges. Track usage separately from a hard spending cap; inspect query profiles before changing warehouse size.

```sql
SELECT CURRENT_ROLE();
SHOW GRANTS;
```

**Check:** Inspect your visible grants; use an authorized administrator only for privilege changes.

## Official references

- https://docs.snowflake.com/en/user-guide/streams-intro
- https://docs.snowflake.com/en/sql-reference/sql/merge
- https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
- https://docs.snowflake.com/en/user-guide/tasks-intro

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

# Databricks and Delta Lake

Use Delta transactions with layered data products; distinguish Databricks platform features from open-source Spark.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Run `merge.sql` in a Databricks SQL warehouse or compatible Delta-enabled environment. Requires table creation privileges; not executed here.

## Topics with worked examples

### Bronze, silver and gold

Bronze preserves source events, silver resolves valid current state, and gold defines business aggregates. Layers describe responsibility, not mandatory physical copies.

```text
bronze: 6 input events
silver: 3 latest valid orders
gold: customer 101=450 cents; 102=250 cents
```

**Check:** Retain reject reasons instead of silently dropping bad data.

### Delta MERGE

Use a unique source row per target key and a source-order condition. Ambiguous source matches can fail; do not depend on runtime-specific duplicate handling.

```sql
SELECT COUNT(*),SUM(amount_cents) FROM de_lab_orders;
```

**Check:** After merge.sql: two rows, 400 cents. Rerun only MERGE for replay.

### History and recovery

History exposes commits; time travel depends on retained logs and data files. Do not assume old versions survive VACUUM.

```sql
DESCRIBE HISTORY de_lab_orders;
SELECT * FROM de_lab_orders VERSION AS OF 0;
```

**Check:** The initial create version is empty; later versions contain inserted/merged rows.

### Governance and jobs

Choose a catalog/schema, grant least privilege and parameterize job inputs. Separate application code from runtime secrets.

```sql
SELECT current_catalog(),current_schema();
```

**Check:** Confirm a sandbox before writing persistent tables.

## Official references

- https://docs.databricks.com/aws/en/delta/merge
- https://docs.databricks.com/aws/en/lakehouse/medallion

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

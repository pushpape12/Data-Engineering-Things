# SQL

Learn relational transformations before scaling to distributed engines. SQL dialects differ; this lab uses SQLite.

[Back to repository index](../README.md)

## Prerequisites and lab

Run `python sql/run.py`; the script creates an in-memory database, loads `examples.sql`, checks totals and exits.

## Topics with worked examples

### Filtering and grouping

Validate before aggregation. Aggregating raw CDC versions overcounts sales.

```sql
SELECT customer_id,SUM(amount_cents) FROM current_orders GROUP BY customer_id;
```

**Check:** Customers 101 and 102 total 450 and 250 cents.

### Joins and cardinality

Join a fact to a unique dimension key. A duplicated dimension key multiplies fact rows.

```sql
SELECT o.order_id,c.segment FROM current_orders o LEFT JOIN customers c ON o.customer_id=c.customer_id;
```

**Check:** Three rows; a missing dimension would preserve its order with NULL segment.

### Windows and CTEs

Rank inside each business key, using a deterministic tie-breaker. Filter rn in an outer query in portable SQL.

```sql
WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY order_id
 ORDER BY updated_at DESC,event_id DESC) rn FROM events WHERE amount_cents>=0
)
SELECT order_id,amount_cents FROM ranked WHERE rn=1;
```

**Check:** Order 1 is 150 cents; its older 100-cent version is excluded.

### Nulls and anti-joins

Use NOT EXISTS to avoid NULL-related surprises with NOT IN.

```sql
SELECT o.order_id FROM current_orders o
WHERE NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id=o.customer_id);
```

**Check:** No orphan orders in the sample.

## Official references

- https://www.sqlite.org/lang.html
- https://www.sqlite.org/windowfunctions.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

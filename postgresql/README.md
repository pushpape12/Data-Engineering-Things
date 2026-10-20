# PostgreSQL

Practice transactional upserts, keys and query plans before using a database as a pipeline control plane.

[Back to repository index](../README.md)

## Prerequisites and lab

Run `upsert.sql` with psql in a sandbox, for example `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f postgresql/upsert.sql`. Provide the connection through your secure environment; the SQL rolls back its table.

## Topics with worked examples

### Constraints and keys

A declared primary key enforces business identity. Composite keys represent multi-column grain.

```sql
CREATE TEMP TABLE step_status(run_id TEXT,step TEXT,status TEXT,PRIMARY KEY(run_id,step));
```

**Check:** Two steps can share run_id; the same run_id/step pair cannot appear twice.

### Version-aware upserts

ON CONFLICT requires an applicable unique constraint. Guard state updates using source order; define equal-timestamp policy explicitly.

```sql
INSERT INTO de_lab_orders VALUES(1,90,'2026-10-01T09:00:00Z')
ON CONFLICT(order_id) DO UPDATE SET amount_cents=EXCLUDED.amount_cents
WHERE EXCLUDED.updated_at>de_lab_orders.updated_at;
```

**Check:** Run inside the example transaction before ROLLBACK; a stale value must not replace 150.

### Indexes and query plans

Index selective lookup/join predicates and inspect actual plans on representative data. Tiny tables may legitimately use sequential scans.

```sql
EXPLAIN SELECT * FROM de_lab_orders WHERE order_id=1;
```

**Check:** Do not conclude an index is unused or broken from a two-row benchmark.

## Official references

- https://www.postgresql.org/docs/current/sql-insert.html
- https://www.postgresql.org/docs/current/using-explain.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

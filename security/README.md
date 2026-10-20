# Security and governance

Separate read, transform, publish and administration privileges in data systems.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Conceptual examples and commented grant templates only. No live security settings are changed.

## Topics with worked examples

### Least privilege

An analytics reader should not own schemas or modify ingestion roles. Evaluate object-level grants for the actual engine.

```sql
-- Snowflake sandbox template; replace identifiers with authorized objects.
-- GRANT USAGE ON DATABASE lab TO ROLE analyst;
-- GRANT USAGE ON SCHEMA lab.curated TO ROLE analyst;
-- GRANT SELECT ON TABLE lab.curated.orders TO ROLE analyst;
```

**Check:** Grant only the necessary object chain; do not grant account administration for a read query.

### Parameter binding

Bind values rather than interpolating user input into SQL. Table identifiers need separate validation; placeholders generally bind values, not identifiers.

```python
cursor.execute("SELECT amount_cents FROM orders WHERE order_id=?", (order_id,))
```

**Check:** The Python lab uses parameter binding and never constructs SQL from input values.

### Sensitive data and lineage

Synthetic examples can be public. Private customer data, query results, employer architecture and credentials must remain in approved systems.

```text
source contract -> transformation version -> output dataset -> owning team
classifications: public / internal / confidential / restricted
```

**Check:** Document lineage and retention; do not copy sensitive values into logs, Git history or dashboards.

## Official references

- https://docs.snowflake.com/en/user-guide/security-access-control-overview
- https://docs.python.org/3/library/sqlite3.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

# Data quality and contracts

Validate structure, business meaning and publication readiness separately.

[Back to repository index](../README.md)

## Prerequisites and lab

Python standard-library lab. Run the ETL first, then check.py. The checker opens the output database read-only.

## Topics with worked examples

### Schema contract

Check required fields, nullability and types at the boundary. Schema drift should trigger an explicit policy rather than accidental casting.

```json
{"order_id":"positive integer","amount_cents":"nonnegative integer","updated_at":"canonical UTC timestamp","event_id":"nonempty string"}
```

**Check:** The Python lab rejects the negative row and reports the CSV line without exposing its payload.

### Grain and reconciliation

Uniqueness alone cannot prove completeness. Compare expected control totals as well as duplicate and null rates.

```bash
python python/etl.py
python data-quality/check.py
```

**Check:** The synthetic fixture must contain 3 orders totalling 700 cents; these are fixture assertions, not a universal production threshold.

### Quality gates and quarantine

Keep failed rows out of curated publication, preserve enough metadata for recovery, and distinguish tolerated rejects from job failure.

```text
extract -> validate -> rejects manifest
valid rows -> merge -> reconciliation -> publish
```

**Check:** This lab tolerates one rejected input; a real pipeline needs a defined reject budget and a quarantine retention policy.

## Official references

- https://docs.getdbt.com/docs/build/data-tests
- https://docs.python.org/3/library/sqlite3.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

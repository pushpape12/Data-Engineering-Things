# Python for data pipelines

Build small, explicit transformations with validation, deterministic ordering and retry-safe writes.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Python 3.11+ with sqlite3; no pip installs. Run `python python/etl.py` from the repository root. Output is a local ignored SQLite file.

## Topics with worked examples

### CSV extraction and schema checks

Stream files with csv.DictReader; validate the contract before converting rows. The executable lab rejects invalid rows without silently treating them as zero.

```python
import csv
with open("datasets/orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))
print(len(rows))
```

**Check:** Six raw events, not six unique orders.

### Types and money

Store integer cents or Decimal amounts rather than binary floating-point currency. Reject negative values for this orders contract.

```python
from decimal import Decimal
cents = int(Decimal("12.50") * 100)
assert cents == 1250
```

**Check:** A currency amount is represented exactly.

### Deduplication and replay

Pick the latest source version per business key, then upsert with a source-order guard. The full lab also detects conflicting payloads for the same version.

```bash
python python/etl.py
python python/etl.py
```

**Check:** Both runs report stored_orders=3 and total_cents=700.

### Transactions and exceptions

Write a batch within a database transaction. A failed row must roll back preceding writes in the same batch.

```bash
python -m unittest discover -s tests -v
```

**Check:** The rollback test inserts a new row before a conflicting row and verifies no partial commit.

## Official references

- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/sqlite3.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

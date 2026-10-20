# Python for data pipelines: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. CSV extraction and schema checks
2. Types and money
3. Deduplication and replay
4. Transactions and exceptions
5. Generators, chunks and memory
6. Retries and concurrency

## 1. CSV extraction and schema checks

### Understand it

CSV values arrive as text. Validate column names, row shape and required values before converting data. Iterate rather than materializing a huge file; retain line numbers or source coordinates for rejected records.

### Practical example

```python
import csv
with open('datasets/orders.csv', newline='') as f:
    reader = csv.DictReader(f)
    for line, row in enumerate(reader, 2):
        if int(row['amount_cents']) < 0:
            print(line, 'negative amount')
```

**Expected result and reasoning:** The fixture reports CSV line 6. This teaching snippet assumes parseable integer text; the full ETL also handles conversion failures.

### Interview question

**How do you process a CSV larger than memory?**

Iterate with csv.DictReader or bounded chunks, validate records, and write batches. Bound intermediate state as well: keeping the newest row for every distinct key can still exceed memory even when input is streamed.

**Common mistake:** Claiming generators make all downstream work memory-free.

**Try it yourself:** Add a malformed integer and route it to a reject list with its line number.

## 2. Types and money

### Understand it

Use integer smallest units or Decimal for money. Decimal from a string preserves decimal intent; Decimal from a float preserves its binary approximation. Specify rounding before converting fractional currency units.

### Practical example

```python
from decimal import Decimal, ROUND_HALF_UP
amount = Decimal('12.345')
rounded = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print(rounded, int(rounded * 100))
```

**Expected result and reasoning:** Output is 12.35 and 1235. This example explicitly chooses half-up rounding, which may differ from an organization's accounting rule.

### Interview question

**Why not store prices as float?**

Binary floats do not exactly represent many decimal fractions. Small errors accumulate or affect equality. Choose a currency scale and rounding policy, store cents or fixed-scale decimals, and preserve that contract through databases and APIs.

**Common mistake:** Converting Decimal to float before loading a decimal destination.

**Try it yourself:** Compare half-up and half-even rounding for 12.345.

## 3. Deduplication and replay

### Understand it

Current-state deduplication chooses one version per business key; event deduplication removes repeated delivery of the same event. They solve different problems. Use canonical source order and detect different payloads for the same version.

### Practical example

```text
e1: order=1, version=10:00, amount=100
e2: order=1, version=10:02, amount=150
e2 replay: same payload
current order amount=150
```

**Expected result and reasoning:** Three deliveries represent two events and one current order. Counting deliveries as orders is incorrect.

### Interview question

**What is the difference between deduplication and an upsert?**

Deduplication resolves repeated or competing input records. An upsert inserts missing destination keys or updates existing keys. You often need both: reduce source matches first and prevent stale updates at the sink.

**Common mistake:** Using dictionary assignment with input order as the source ordering contract.

**Try it yourself:** Shuffle the fixture and confirm current-state totals are unchanged.

## 4. Transactions and exceptions

### Understand it

A transaction defines the unit that commits or rolls back. Catch errors only where a useful recovery decision exists; swallowing an exception can mark a failed batch successful. Keep source progress separate from uncommitted writes.

### Practical example

```python
import sqlite3
with sqlite3.connect(':memory:') as db:
    db.execute('CREATE TABLE t(id INTEGER PRIMARY KEY, amount INTEGER CHECK(amount>=0))')
    try:
        with db:
            db.execute('INSERT INTO t VALUES(1,150)')
            db.execute('INSERT INTO t VALUES(2,-1)')
    except sqlite3.IntegrityError:
        pass
    print(db.execute('SELECT COUNT(*) FROM t').fetchone()[0])
```

**Expected result and reasoning:** The output is 0: the invalid second insert rolls back the first. The table exists because schema creation happened before the DML transaction.

### Interview question

**Where should you catch a database error?**

At the boundary where you can rollback, classify transient versus permanent failures, emit sanitized diagnostics and decide whether to retry. Do not return success unless the intended transaction committed.

**Common mistake:** Committing each row when the business unit is the entire batch.

**Try it yourself:** Explain how a crash after commit but before task success causes replay.

## 5. Generators, chunks and memory

### Understand it

Generators defer production of items and support bounded pipelines. They do not automatically stream database drivers or aggregations. Dictionary-based grouping still uses memory proportional to distinct keys.

### Practical example

```python
def positive_amounts(rows):
    for row in rows:
        amount = int(row['amount_cents'])
        if amount >= 0:
            yield amount
print(sum(positive_amounts([{'amount_cents':'100'}, {'amount_cents':'-1'}])))
```

**Expected result and reasoning:** Output is 100. The aggregation maintains one running sum, not a list of every amount.

### Interview question

**Why can a generator pipeline still run out of memory?**

A downstream list(), sorted(), group-by dictionary or buffered client can retain the complete dataset. Measure both batch size and state cardinality; push grouping to a suitable engine when needed.

**Common mistake:** Calling list(generator) immediately and claiming streaming behavior.

**Try it yourself:** Identify the memory growth of latest-version-per-customer state.

## 6. Retries and concurrency

### Understand it

Retry bounded transient failures with backoff, jitter and timeouts. A timeout does not prove the server failed to commit. Idempotency keys or destination constraints are needed before retries of side effects.

### Practical example

```text
request create order -> server commits -> response lost
client timeout -> retry with same idempotency key
server returns existing logical result
```

**Expected result and reasoning:** The retry returns one logical order, not two. A new random idempotency key per attempt defeats this pattern.

### Interview question

**Would you use threads or processes for a pipeline?**

For waiting on independent I/O, bounded threads or async clients can help. CPU-heavy pure Python often benefits from processes, subject to serialization and memory overhead. Bound concurrency using service quotas and connection-pool capacity.

**Common mistake:** Retrying every exception indefinitely or parallelizing writes without an ordering policy.

**Try it yourself:** Design a retry policy for 429 responses and a separate policy for schema errors.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

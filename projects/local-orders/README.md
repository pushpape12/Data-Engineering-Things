# Project: retry-safe order ingestion

[Back to index](../../README.md)

## Problem

A source retries messages, sends newer versions of the same order and occasionally
sends invalid values. Produce one current row per order and correct customer totals.

## Architecture

1. Read the synthetic CSV with an explicit five-column contract.
2. Validate types, positive IDs, nonnegative integer cents and canonical UTC time.
3. Report rejected line numbers and reasons without printing source payloads.
4. Choose the newest `(updated_at,event_id)` per order; reject conflicting equal keys.
5. Upsert current rows in one SQLite transaction, rejecting stale updates.
6. Validate fixture counts and business totals before considering the run complete.

## Run from repository root

```bash
python python/etl.py
python python/etl.py
python sql/run.py
python kafka/replay.py
python data-quality/check.py
python -m unittest discover -s tests -v
```

Expected ETL summary on a fresh or previously replayed fixture database:
`valid_input_rows=5`, `rejected_rows=1`, `batch_current_orders=3`,
`stored_orders=3`, `total_cents=700`.

The database persists under ignored `output/`. To run against a fresh database
without deleting existing work, pass `--database output/another-lab.db`.
The quality checker specifically checks `output/orders.db`.

## Correctness boundaries

This is a single-process, insert/update educational lab. It does not implement
source deletes, distributed exactly-once processing, a durable quarantine store,
an external source watermark, or a CDC log sequence. Lexical event IDs provide a
fixture-specific tie-breaker. Define a true source sequence and concurrency
strategy before adapting this to production. Only a current version is retained;
retain an event log separately when audit/reconstruction is required.

## Extend as practical exercises

- Add delete/tombstone events and verify late updates cannot resurrect deleted rows.
- Partition input by run interval and persist a checkpoint only after successful load.
- Send accepted/rejected rows to separate durable destinations with a manifest.
- Port the state merge to Snowflake or Delta, retaining source-order guards.
- Add a source schema version and reject incompatible changes with a clear reason.

These are extension exercises, not features claimed by the current implementation.

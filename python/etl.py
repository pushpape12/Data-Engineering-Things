"""CSV -> validated latest order state -> transactional SQLite upsert.
Run from the repository root: python python/etl.py
"""
from __future__ import annotations
import argparse
import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"order_id", "customer_id", "amount_cents", "updated_at", "event_id"}

def normalize(raw):
    row = {key: int(raw[key]) for key in ("order_id", "customer_id", "amount_cents")}
    if row["order_id"] <= 0 or row["customer_id"] <= 0 or row["amount_cents"] < 0:
        raise ValueError("IDs must be positive and amount_cents nonnegative")
    timestamp = raw["updated_at"]
    if datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ") != timestamp:
        raise ValueError("Timestamp must use canonical UTC format")
    if not raw["event_id"].strip():
        raise ValueError("event_id is required")
    return {**row, "updated_at": timestamp, "event_id": raw["event_id"]}

def extract(path):
    good, rejected = [], []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != FIELDS:
            raise ValueError("Unexpected CSV columns")
        for line, raw in enumerate(reader, 2):
            try:
                good.append(normalize(raw))
            except (ValueError, TypeError, KeyError) as error:
                rejected.append({"line": line, "reason": str(error)})
    return good, rejected

def latest(rows):
    result = {}
    for row in rows:
        old = result.get(row["order_id"])
        key = (row["updated_at"], row["event_id"])
        if old is not None and key == (old["updated_at"], old["event_id"]) and old != row:
            raise ValueError("Conflicting payload for identical order/version key")
        if old is None or key > (old["updated_at"], old["event_id"]):
            result[row["order_id"]] = row
    return [result[key] for key in sorted(result)]

def load(connection, rows):
    connection.execute("""CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
        amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
        updated_at TEXT NOT NULL, event_id TEXT NOT NULL)""")
    with connection:
        for row in rows:
            existing = connection.execute(
                "SELECT customer_id, amount_cents, updated_at, event_id FROM orders WHERE order_id=?",
                (row["order_id"],),
            ).fetchone()
            if existing and existing[2:] == (row["updated_at"], row["event_id"]):
                if existing[:2] != (row["customer_id"], row["amount_cents"]):
                    raise ValueError("Conflicting persisted payload for identical order/version key")
            connection.execute("""INSERT INTO orders VALUES (
                :order_id, :customer_id, :amount_cents, :updated_at, :event_id)
                ON CONFLICT(order_id) DO UPDATE SET
                customer_id=excluded.customer_id, amount_cents=excluded.amount_cents,
                updated_at=excluded.updated_at, event_id=excluded.event_id
                WHERE (excluded.updated_at, excluded.event_id) >
                      (orders.updated_at, orders.event_id)""", row)

def run(source, database):
    rows, rejects = extract(source)
    current = latest(rows)
    with sqlite3.connect(database) as connection:
        load(connection, current)
        count, total = connection.execute("SELECT COUNT(*), COALESCE(SUM(amount_cents),0) FROM orders").fetchone()
    return {"valid_input_rows": len(rows), "rejected_rows": len(rejects),
            "batch_current_orders": len(current), "stored_orders": count,
            "total_cents": total, "rejects": rejects}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "datasets/orders.csv")
    parser.add_argument("--database", type=Path, default=ROOT / "output/orders.db")
    args = parser.parse_args()
    args.database.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(run(args.source, args.database), indent=2))

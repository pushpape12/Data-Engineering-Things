"""Read-only quality checks on the local pipeline output."""
import sqlite3
from pathlib import Path
path = Path(__file__).resolve().parents[1] / "output/orders.db"
if not path.exists():
    raise SystemExit("Run python python/etl.py first")
with sqlite3.connect(path.as_uri()+"?mode=ro", uri=True) as db:
    count, total = db.execute("SELECT COUNT(*),SUM(amount_cents) FROM orders").fetchone()
    bad = db.execute("SELECT COUNT(*) FROM orders WHERE amount_cents<0 OR customer_id IS NULL").fetchone()[0]
    if (count, total, bad) != (3, 700, 0):
        raise SystemExit(f"Fixture contract failed: count={count},total={total},invalid={bad}")
print("PASS: 3 current orders, 700 cents, 0 invalid rows")

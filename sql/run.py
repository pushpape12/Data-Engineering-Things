import sqlite3
from pathlib import Path
with sqlite3.connect(":memory:") as db:
    db.executescript(Path(__file__).with_name("examples.sql").read_text())
    rows = db.execute("SELECT customer_id,SUM(amount_cents) FROM current_orders GROUP BY customer_id ORDER BY customer_id").fetchall()
    if rows != [(101, 450), (102, 250)]:
        raise RuntimeError(f"Unexpected totals: {rows}")
    print(rows)

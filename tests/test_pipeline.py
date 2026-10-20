import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("etl", ROOT / "python/etl.py")
etl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(etl)

class PipelineTests(unittest.TestCase):
    def test_fixture_and_replay(self):
        with tempfile.TemporaryDirectory() as folder:
            db = Path(folder) / "orders.db"
            first = etl.run(ROOT / "datasets/orders.csv", db)
            second = etl.run(ROOT / "datasets/orders.csv", db)
            self.assertEqual(first, second)
            self.assertEqual((first["stored_orders"], first["total_cents"], first["rejected_rows"]), (3, 700, 1))

    def test_late_event_does_not_regress_state(self):
        rows, _ = etl.extract(ROOT / "datasets/orders.csv")
        with sqlite3.connect(":memory:") as db:
            etl.load(db, etl.latest(rows))
            etl.load(db, [rows[0]])
            self.assertEqual(db.execute("SELECT amount_cents FROM orders WHERE order_id=1").fetchone()[0], 150)

    def test_conflict_rolls_back_entire_batch(self):
        row = dict(order_id=1, customer_id=101, amount_cents=100,
                   updated_at="2026-10-01T10:00:00Z", event_id="e1")
        with sqlite3.connect(":memory:") as db:
            etl.load(db, [row])
            with self.assertRaises(ValueError):
                etl.load(db, [{**row, "order_id": 2}, {**row, "amount_cents": 200}])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 1)

    def test_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            etl.normalize(dict(order_id="1", customer_id="1", amount_cents="100",
                               updated_at="yesterday", event_id="e1"))

    def test_conflicting_batch_version(self):
        rows, _ = etl.extract(ROOT / "datasets/orders.csv")
        with self.assertRaises(ValueError):
            etl.latest([rows[0], {**rows[0], "amount_cents": 999}])

if __name__ == "__main__":
    unittest.main()

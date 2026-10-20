-- SQLite 3.25+ dialect. In-memory exercise, executed by sql/run.py.
CREATE TABLE events(order_id INTEGER, customer_id INTEGER, amount_cents INTEGER,
 updated_at TEXT, event_id TEXT);
INSERT INTO events VALUES
 (1,101,100,'2026-10-01T10:00:00Z','e1'),
 (2,102,250,'2026-10-01T10:01:00Z','e2'),
 (1,101,150,'2026-10-01T10:02:00Z','e3'),
 (3,101,300,'2026-10-01T10:03:00Z','e4'),
 (4,103,-50,'2026-10-01T10:04:00Z','e5'),
 (2,102,250,'2026-10-01T10:01:00Z','e2');
CREATE VIEW current_orders AS
 WITH ranked AS (
 SELECT *, ROW_NUMBER() OVER (
 PARTITION BY order_id ORDER BY updated_at DESC,event_id DESC) AS rn
 FROM events WHERE amount_cents >= 0)
 SELECT order_id,customer_id,amount_cents,updated_at,event_id FROM ranked WHERE rn=1;
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, segment TEXT);
INSERT INTO customers VALUES(101,'retail'),(102,'business');

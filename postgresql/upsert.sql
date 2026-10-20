-- PostgreSQL. Entire lab rolled back; use an isolated sandbox database.
BEGIN;
CREATE TEMP TABLE de_lab_orders (
 order_id BIGINT PRIMARY KEY, amount_cents BIGINT NOT NULL CHECK(amount_cents>=0),
 updated_at TIMESTAMPTZ NOT NULL
);
INSERT INTO de_lab_orders VALUES(1,100,'2026-10-01T10:00:00Z');
INSERT INTO de_lab_orders VALUES(1,150,'2026-10-01T10:02:00Z'),(2,250,'2026-10-01T10:01:00Z')
ON CONFLICT(order_id) DO UPDATE
 SET amount_cents=EXCLUDED.amount_cents,updated_at=EXCLUDED.updated_at
 WHERE EXCLUDED.updated_at>de_lab_orders.updated_at;
SELECT COUNT(*),SUM(amount_cents) FROM de_lab_orders; -- 2,400
EXPLAIN SELECT * FROM de_lab_orders WHERE order_id=1;
ROLLBACK;

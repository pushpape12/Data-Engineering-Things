-- Databricks SQL / Delta. Run in an existing sandbox catalog and schema.
-- These new persistent table names must not already exist.
CREATE TABLE de_lab_orders (order_id BIGINT,amount_cents BIGINT,updated_at TIMESTAMP) USING DELTA;
INSERT INTO de_lab_orders VALUES(1,100,TIMESTAMP '2026-10-01 10:00:00');
CREATE TEMP VIEW de_lab_updates AS SELECT * FROM VALUES
 (1L,150L,TIMESTAMP '2026-10-01 10:02:00'),
 (2L,250L,TIMESTAMP '2026-10-01 10:01:00') AS s(order_id,amount_cents,updated_at);
MERGE INTO de_lab_orders t USING de_lab_updates s ON t.order_id=s.order_id
WHEN MATCHED AND s.updated_at>t.updated_at THEN
 UPDATE SET amount_cents=s.amount_cents,updated_at=s.updated_at
WHEN NOT MATCHED THEN INSERT (order_id,amount_cents,updated_at)
 VALUES(s.order_id,s.amount_cents,s.updated_at);
SELECT COUNT(*),SUM(amount_cents) FROM de_lab_orders; -- 2,400
DESCRIBE HISTORY de_lab_orders;
-- Cleanup after inspection: DROP TABLE de_lab_orders;

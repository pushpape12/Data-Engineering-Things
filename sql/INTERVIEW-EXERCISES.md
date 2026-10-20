# SQL interview coding workbook

[SQL notes](INTERVIEW.md) · [Revision hub](../INTERVIEW-PREP.md)

Attempt the problem before opening its solution. All solutions below are self-contained **SQLite 3.25+** queries and use synthetic in-memory CTE data. No permanent tables are modified. Expected results are reasoned worked answers; these new queries were not executed in this revision.

## 1. Second-highest distinct salary

Return every employee at the second-highest distinct salary. Ties must not consume extra salary positions.

<details>
<summary>Solution and expected output</summary>

```sql
WITH employees(name,salary) AS (
 VALUES ('A',100),('B',100),('C',90),('D',80)
),
ranked AS (
 SELECT name,salary,DENSE_RANK() OVER(ORDER BY salary DESC) AS r
 FROM employees
)
SELECT name,salary FROM ranked WHERE r=2 ORDER BY name;
```

Expected: **C,90**. ROW_NUMBER would incorrectly select another 100-salary employee if used without first resolving distinct salaries.
</details>

## 2. Latest order state

Resolve multiple versions, including repeated delivery. Use event_id as a deterministic fixture tie-breaker. Return the complete selected row, not independently aggregated field maxima.

<details>
<summary>Solution and expected output</summary>

```sql
WITH events(order_id,amount,updated_at,event_id) AS (
 VALUES (1,100,'2026-10-01T10:00:00Z','e1'),
        (1,150,'2026-10-01T10:02:00Z','e2'),
        (1,150,'2026-10-01T10:02:00Z','e2'),
        (2,250,'2026-10-01T10:01:00Z','e3')
),
ranked AS (
 SELECT *,ROW_NUMBER() OVER(
  PARTITION BY order_id ORDER BY updated_at DESC,event_id DESC
 ) rn FROM events
)
SELECT order_id,amount,updated_at,event_id
FROM ranked WHERE rn=1 ORDER BY order_id;
```

Expected: **(1,150,10:02,e2)** and **(2,250,10:01,e3)**, with full timestamps as in input. Different payloads for the same version require explicit conflict detection upstream; ranking alone cannot establish which is true.
</details>

## 3. Top two orders per customer

Return at most two orders for each customer, descending by amount; break ties by smaller order_id. If the requirement instead means all orders tied in the top two distinct amounts, explain the ranking change.

<details>
<summary>Solution and expected output</summary>

```sql
WITH orders(customer_id,order_id,amount) AS (
 VALUES (101,1,150),(101,2,300),(101,3,300),(102,4,250)
),
ranked AS (
 SELECT *,ROW_NUMBER() OVER(
  PARTITION BY customer_id ORDER BY amount DESC,order_id
 ) rn FROM orders
)
SELECT customer_id,order_id,amount
FROM ranked WHERE rn<=2 ORDER BY customer_id,rn;
```

Expected: **(101,2,300),(101,3,300),(102,4,250)**. For top two distinct amounts with all ties, use DENSE_RANK ordered by amount only; customer 101 would then also include order 1 at 150.
</details>

## 4. Missing days without a NULL trap

Find calendar days with no delivery record, even if the deliveries table contains a NULL day.

<details>
<summary>Solution and expected output</summary>

```sql
WITH calendar(day) AS (
 VALUES ('2026-10-01'),('2026-10-02'),('2026-10-03')
),
deliveries(day) AS (VALUES ('2026-10-01'),(NULL))
SELECT c.day FROM calendar c
WHERE NOT EXISTS (SELECT 1 FROM deliveries d WHERE d.day=c.day)
ORDER BY c.day;
```

Expected: **2026-10-02 and 2026-10-03**. A naive NOT IN sees the NULL and fails to produce these unmatched days.
</details>

## 5. Diagnose revenue multiplication

An order has two line items. Explain why summing order-level revenue after joining to line items is wrong, then compute the actual order-level total.

<details>
<summary>Solution and expected output</summary>

```sql
WITH orders(order_id,amount) AS (VALUES (1,1000)),
items(order_id,sku) AS (VALUES (1,'A'),(1,'B'))
SELECT SUM(o.amount) AS wrong_total
FROM orders o JOIN items i ON i.order_id=o.order_id;
```

Expected wrong total: **2000**. Correct order-grain total:

```sql
WITH orders(order_id,amount) AS (VALUES (1,1000))
SELECT SUM(amount) AS correct_total FROM orders;
```

Expected: **1000**. SUM(DISTINCT amount) is not a general fix: two real different orders can have the same amount. Aggregate item amounts at item grain, or preserve order grain before summing the order measure.
</details>

## 6. Running daily revenue

Collapse repeated dates to day grain, then compute a running total. Explain why the preaggregation matters.

<details>
<summary>Solution and expected output</summary>

```sql
WITH sales(day,amount) AS (
 VALUES ('2026-10-01',100),('2026-10-01',150),('2026-10-02',250)
),
daily AS (SELECT day,SUM(amount) AS revenue FROM sales GROUP BY day)
SELECT day,revenue,
 SUM(revenue) OVER(
  ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
 ) AS running
FROM daily ORDER BY day;
```

Expected: **(2026-10-01,250,250),(2026-10-02,250,500)**. The output grain is one row per day, so no ambiguity from same-day row ordering remains.
</details>

## Before you say “done”

State the SQL dialect, input grain, key/NULL policy and expected output. Explain the complexity/plan at a useful level, then test empty input, duplicate keys and ties. Correctness precedes optimization.

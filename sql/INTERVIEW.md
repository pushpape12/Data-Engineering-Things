# SQL: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Filtering and grouping
2. Joins and cardinality
3. Windows and CTEs
4. Nulls and anti-joins
5. Running totals and window frames
6. SCD Type 1 and Type 2
7. Query optimization

## 1. Filtering and grouping

### Understand it

WHERE filters rows before grouping; HAVING filters aggregate groups. COUNT(*) counts rows, COUNT(column) ignores NULLs, and SUM of no rows is normally NULL. Aggregate current state rather than all historical versions.

### Practical example

```sql
-- After loading sql/examples.sql in a SQLite session:
SELECT customer_id, SUM(amount_cents) AS revenue
FROM current_orders
GROUP BY customer_id
HAVING SUM(amount_cents) >= 300;
```

**Expected result and reasoning:** Only customer 101 appears, with 450 cents; customer 102 has 250.

### Interview question

**What is the difference between WHERE and HAVING?**

WHERE restricts input rows, while HAVING restricts grouped output. For a date-limited revenue query, filter the date in WHERE and the minimum total in HAVING.

**Common mistake:** Trying to use SUM(amount_cents) in WHERE.

**Try it yourself:** Return customers with at least two current orders and total revenue above 400.

## 2. Joins and cardinality

### Understand it

A join produces one output for every matching pair. LEFT JOIN retains unmatched left rows, but filtering a right-side column in WHERE can remove those NULL-extended rows. Validate dimension uniqueness before joining.

### Practical example

```sql
-- SQLite; standalone example:
WITH orders(id,customer_id) AS (VALUES(1,101),(2,102)),
dim(customer_id,segment) AS (VALUES(101,'A'),(101,'B'))
SELECT o.id,d.segment FROM orders o
LEFT JOIN dim d ON o.customer_id=d.customer_id;
```

**Expected result and reasoning:** Three rows: (1,A), (1,B), (2,NULL). The nonunique dimension duplicates order 1.

### Interview question

**How can a LEFT JOIN behave like an INNER JOIN?**

A WHERE predicate such as d.segment='A' excludes unmatched rows because NULL does not satisfy it. Put a right-side filter in the ON clause when preserving all left rows is intended.

**Common mistake:** Assuming LEFT JOIN always preserves exactly the left row count.

**Try it yourself:** Add the segment filter in ON and then WHERE; explain the different results.

## 3. Windows and CTEs

### Understand it

A window calculates across related rows without collapsing them. ROW_NUMBER assigns unique positions; RANK leaves gaps after ties; DENSE_RANK does not. CTEs improve structure but are not a portable guarantee of materialization.

### Practical example

```sql
WITH x(person,score) AS (VALUES('A',100),('B',100),('C',90))
SELECT person,score,
 ROW_NUMBER() OVER(ORDER BY score DESC,person) rn,
 RANK() OVER(ORDER BY score DESC) rnk,
 DENSE_RANK() OVER(ORDER BY score DESC) dense
FROM x ORDER BY score DESC,person;
```

**Expected result and reasoning:** A=(1,1,1), B=(2,1,1), C=(3,3,2), with columns rn/rnk/dense.

### Interview question

**How do you find the second-highest distinct salary?**

Use DENSE_RANK over salary descending and filter rank=2 in an outer query. Decide whether to return all tied employees or only the salary amount.

**Common mistake:** Adding employee_id to the ranking order when the requirement is distinct salary rank.

**Try it yourself:** Write top two orders per customer with deterministic tie-breaking.

## 4. Nulls and anti-joins

### Understand it

NULL represents unknown/missing information and uses three-valued logic. Comparisons to NULL are not true; use IS NULL. NOT IN can exclude everything if its candidate set includes NULL.

### Practical example

```sql
WITH a(id) AS (VALUES(1),(2)), b(id) AS (VALUES(1),(NULL))
SELECT a.id FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.id=a.id);
```

**Expected result and reasoning:** Returns 2. Replacing NOT EXISTS with id NOT IN (SELECT id FROM b) returns no rows for this fixture.

### Interview question

**Why did NOT IN return no unmatched records?**

A NULL in the candidate set makes comparisons for nonmatching values unknown. Use NOT EXISTS with a defined equality condition, or explicitly remove NULL when that matches the business semantics.

**Common mistake:** Using = NULL or replacing every NULL with zero.

**Try it yourself:** Explain why a missing amount is different from a genuine zero payment.

## 5. Running totals and window frames

### Understand it

Specify the frame for row-by-row accumulation. Default RANGE behavior can include peer rows with the same ordering value together. A deterministic row order plus ROWS makes the intention explicit.

### Practical example

```sql
WITH sales(day,id,amount) AS (VALUES('2026-10-01',1,100),('2026-10-01',2,150),('2026-10-02',3,250))
SELECT id,SUM(amount) OVER(ORDER BY day,id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) running
FROM sales ORDER BY day,id;
```

**Expected result and reasoning:** Running totals are 100,250,500. Both rows on the first date do not jump immediately to 250.

### Interview question

**Why can running totals repeat for tied dates?**

With a peer-inclusive RANGE frame, rows sharing the ordering value can see the same frame. Choose the desired daily or per-row grain, preaggregate if appropriate, and specify ordering/frame intentionally.

**Common mistake:** Relying on the physical input order for tied values.

**Try it yourself:** Compute daily revenue first, then its running total.

## 6. SCD Type 1 and Type 2

### Understand it

Type 1 overwrites an attribute. Type 2 preserves validity intervals and usually uses a surrogate dimension key. A historical fact must match the dimension version applicable to its event time.

### Practical example

```sql
-- Hypothetical dimension rows:
-- customer 101, city='Delhi', valid_from='2026-01-01', valid_to='2026-06-01'
-- customer 101, city='Hyderabad', valid_from='2026-06-01', valid_to=NULL
-- Temporal join predicate:
-- f.customer_id=d.customer_id AND f.event_time>=d.valid_from
-- AND (f.event_time<d.valid_to OR d.valid_to IS NULL)
```

**Expected result and reasoning:** A May fact uses Delhi; a July fact uses Hyderabad. Half-open intervals avoid double matches at the boundary.

### Interview question

**How do you implement historical customer attributes?**

Choose a stable business key, a version surrogate key and nonoverlapping validity ranges. Close the previous version and insert the new one transactionally; address late corrections and hard deletes explicitly.

**Common mistake:** Joining facts only to is_current=true when historical attribution is required.

**Try it yourself:** Describe what happens to a historical fact when an address change arrives late.

## 7. Query optimization

### Understand it

Inspect the plan before changing code or compute. Reduce scanned columns/rows, verify join keys and cardinality, and distinguish CPU, I/O, network and skew bottlenecks. An index strategy for PostgreSQL is not Snowflake's storage strategy.

### Practical example

```sql
-- SQLite lab:
EXPLAIN QUERY PLAN SELECT * FROM customers WHERE customer_id=101;
```

**Expected result and reasoning:** The primary key permits a targeted lookup. Exact plan text varies by engine/version; tiny scans can be reasonable.

### Interview question

**How would you optimize a slow join?**

Establish a reproducible baseline, inspect actual row counts and plan, prune input, ensure compatible join types and choose appropriate physical layout/indexes. Recheck output correctness and measured performance.

**Common mistake:** Presenting SELECT DISTINCT or a bigger warehouse as the universal fix.

**Try it yourself:** Compare plan and output counts before and after adding a duplicated dimension row.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

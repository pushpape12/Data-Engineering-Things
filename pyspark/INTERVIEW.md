# Apache Spark and PySpark: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Schemas and lazy evaluation
2. Windows and deduplication
3. Joins and shuffles
4. Partitions and output
5. Skew diagnosis
6. Caching and collect

## 1. Schemas and lazy evaluation

### Understand it

Spark builds a logical plan from transformations and executes work at actions. Explicit schemas avoid an inference pass and accidental types, but they do not replace validation of malformed rows. Inspect plans rather than assuming a transformation is free.

### Practical example

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[2]').appName('interview').getOrCreate()
df = spark.createDataFrame([(1,150),(2,250)],'order_id INT, amount_cents INT')
filtered = df.filter('amount_cents >= 200')
filtered.explain()
filtered.show()
```

**Expected result and reasoning:** Only order 2 is displayed. explain shows planning; show triggers result computation in a compatible local Spark runtime.

### Interview question

**What is lazy evaluation useful for?**

It lets Spark optimize a combined plan, push filters/projections where supported and avoid unnecessary intermediate materialization. Repeated actions may recompute work unless persisted or otherwise reused.

**Common mistake:** Calling count repeatedly to inspect every pipeline step.

**Try it yourself:** Explain why schema inference can increase startup work on files.

## 2. Windows and deduplication

### Understand it

Use a per-key order to select the latest record. dropDuplicates chooses unique key combinations but does not promise the highest timestamp. Window operations can shuffle and sort substantial data.

### Practical example

```python
from pyspark.sql import Window,functions as F
w = Window.partitionBy('order_id').orderBy(F.desc('updated_at'),F.desc('event_id'))
# raw must have the sample dataset schema:
current = raw.filter('amount_cents >= 0').withColumn('rn',F.row_number().over(w)).filter('rn=1').drop('rn')
```

**Expected result and reasoning:** With raw loaded as in orders.py, three current orders remain and amount total is 700.

### Interview question

**How do you keep the latest event per key?**

Define a trustworthy source-order column and deterministic tie policy, validate conflicts, then rank/filter per key. Distinguish current-state batch resolution from bounded streaming deduplication.

**Common mistake:** Using processing arrival time as event version when source updates arrive late.

**Try it yourself:** Add equal timestamps with conflicting payloads and define rejection behavior.

## 3. Joins and shuffles

### Understand it

A shuffle redistributes rows by key across executors. Broadcast can avoid shuffling a sufficiently small build side, but a large broadcast can exhaust memory. Adaptive planning may adjust strategies based on execution statistics.

### Practical example

```python
dim = spark.createDataFrame([(101,'retail'),(102,'business')],'customer_id INT, segment STRING')
# current from the order lab:
joined = current.join(F.broadcast(dim),'customer_id','left')
joined.explain('formatted')
```

**Expected result and reasoning:** The example dimension is small and joins to three orders. The physical plan should be inspected for the selected strategy.

### Interview question

**How do you optimize a large fact-to-small-dimension join?**

Filter/project first, verify dimension uniqueness, assess actual size, and use broadcast when safe. Measure the actual plan, spilled data, task distribution and correctness.

**Common mistake:** Broadcasting based only on row count when rows contain very large payloads.

**Try it yourself:** Explain why joining on a heavily skewed NULL key can create a long-running task.

## 4. Partitions and output

### Understand it

Input partitions, shuffle partitions and storage partitions are different concepts. repartition redistributes data; coalesce usually reduces execution partitions without a full balancing shuffle. partitionBy controls output directory layout, not an exact file count.

### Practical example

```python
# After current is built:
current.repartition(2).write.mode('overwrite').parquet('output/spark-orders-lab')
```

**Expected result and reasoning:** The dedicated lab path receives multiple output files/metadata. It is not guaranteed to contain exactly two data files under every runtime optimization.

### Interview question

**repartition versus coalesce?**

Use repartition when balanced redistribution is worth a shuffle. Use coalesce for reducing partitions when existing distribution is acceptable. Judge task sizes and file sizes, not a universal partition number.

**Common mistake:** Using coalesce(1) to solve every small-file problem.

**Try it yourself:** Design an output layout for a terabyte/day workload with date filters.

## 5. Skew diagnosis

### Understand it

Skew concentrates work on a few keys/partitions. Increasing all partition counts may not split a single hot key. Inspect task duration, input/shuffle sizes and key frequency before choosing mitigation.

### Practical example

```python
# Example diagnosis on an existing DataFrame:
raw.groupBy('customer_id').count().orderBy(F.desc('count')).show(10)
```

**Expected result and reasoning:** A hot key appears disproportionately often. The six-row fixture is too small for a meaningful performance benchmark.

### Interview question

**How do you fix one reducer taking much longer?**

Check for skew and spill, filter invalid hot keys, broadcast a small side, use supported adaptive skew handling, or salt with a correct recombination strategy. Preserve join semantics when salting.

**Common mistake:** Salting only one join side or forgetting to recombine aggregates.

**Try it yourself:** Explain a two-stage salted SUM and why averages need sum plus count.

## 6. Caching and collect

### Understand it

Persist only reused, expensive intermediates that justify storage. Caching is lazy until materialized and consumes executor resources. collect sends all rows to driver memory; use bounded previews or distributed writes for large results.

### Practical example

```python
current.cache()
current.count()  # materializes for this tiny lab
current.groupBy('customer_id').sum('amount_cents').show()
current.unpersist()
```

**Expected result and reasoning:** The aggregate uses the cached current-state result where available; unpersist releases it. This is a teaching example, not evidence caching improves a tiny job.

### Interview question

**When should you cache a DataFrame?**

When reuse saves more recomputation than the memory/disk and materialization overhead. Inspect storage and eviction; cache is not a substitute for an efficient plan.

**Common mistake:** Calling collect on production-scale data for debugging.

**Try it yourself:** Compare repeated action costs with and without persistence on representative data.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

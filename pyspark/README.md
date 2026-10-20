# Apache Spark and PySpark

Use distributed DataFrames when data volume and shuffle work justify a cluster. Start with explicit schemas and built-in expressions.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Optional runtime lab: Python, a compatible JDK and PySpark. In a separate environment install `pyspark>=3.5,<5`, then run `python pyspark/orders.py`. Choose compatible Java/Python versions for your selected Spark release; not executed here.

## Topics with worked examples

### Schemas and lazy evaluation

Reads and transformations build a plan. Actions such as show/count collect results. Treat malformed input handling as a data-contract decision.

```python
raw = spark.read.option("header", True).schema(schema).csv(path)
raw.printSchema()
```

**Check:** The executable script defines every field explicitly; timestamps are canonical UTC strings in this fixture.

### Windows and deduplication

dropDuplicates alone does not choose the newest record. Use an ordered window for current-state snapshots.

```python
current = valid.withColumn("rn", F.row_number().over(window)).filter("rn=1").drop("rn")
```

**Check:** Three current orders remain.

### Joins and shuffles

Broadcast only genuinely small dimensions. Inspect the plan and avoid broadcasting a large fact table.

```python
dim = spark.createDataFrame([(101,"retail"),(102,"business")], "customer_id INT, segment STRING")
current.join(F.broadcast(dim),"customer_id","left").explain("formatted")
```

**Check:** Look for a broadcast join in a compatible Spark plan.

### Partitions and output

Repartition shuffles; coalesce usually reduces partitions without a full rebalance. Excess partitions create small files; one partition can bottleneck.

```python
current.repartition(2).write.mode("overwrite").parquet("output/spark-orders")
```

**Check:** Opt-in output for this small fixture; do not overwrite a production path.

## Official references

- https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html
- https://spark.apache.org/docs/latest/sql-performance-tuning.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

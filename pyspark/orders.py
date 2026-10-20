from pathlib import Path
from pyspark.sql import SparkSession, Window, functions as F
spark = SparkSession.builder.master("local[2]").appName("de-orders-lab").getOrCreate()
try:
    path = str(Path(__file__).resolve().parents[1] / "datasets/orders.csv")
    schema = "order_id INT, customer_id INT, amount_cents INT, updated_at STRING, event_id STRING"
    raw = spark.read.option("header", True).schema(schema).csv(path)
    valid = raw.filter((F.col("order_id") > 0) & (F.col("customer_id") > 0) & (F.col("amount_cents") >= 0))
    window = Window.partitionBy("order_id").orderBy(F.desc("updated_at"), F.desc("event_id"))
    current = valid.withColumn("rn", F.row_number().over(window)).filter("rn=1").drop("rn")
    current.orderBy("order_id").show()
    result = current.agg(F.count("*").alias("n"), F.sum("amount_cents").alias("total")).first()
    if (result.n, result.total) != (3, 700):
        raise RuntimeError(f"Unexpected totals: {result}")
    current.explain("formatted")
finally:
    spark.stop()

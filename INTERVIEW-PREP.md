# Data engineering interview revision hub

[Repository home](README.md) · [Learning path](LEARNING-PATH.md) · [SQL coding workbook](sql/INTERVIEW-EXERCISES.md)

Use this as a study reference rather than a list of buzzwords. Each of the **92 topic sections** contains:
- A plain-language explanation and decision criteria.
- A practical worked example with context/dialect.
- Expected output or an explicit interpretation when output is environment-dependent.
- An interview question and a suggested answer.
- A common mistake and an exercise to attempt yourself.

All **81 topics** in the original technology guides are expanded here, with 11 additional interview topics. Examples are synthetic and do not claim personal employment experience.

## Choose a technology

| Study notes | Topics | Practical lab |
|---|---:|---|
| [Python for data pipelines](python/INTERVIEW.md) | 6 | [Run/setup](python/README.md) |
| [SQL](sql/INTERVIEW.md) | 7 | [Run/setup](sql/README.md) |
| [Data engineering foundations](fundamentals/INTERVIEW.md) | 4 | [Run/setup](fundamentals/README.md) |
| [Snowflake](snowflake/INTERVIEW.md) | 9 | [Run/setup](snowflake/README.md) |
| [Apache Spark and PySpark](pyspark/INTERVIEW.md) | 6 | [Run/setup](pyspark/README.md) |
| [Databricks and Delta Lake](databricks/INTERVIEW.md) | 4 | [Run/setup](databricks/README.md) |
| [AWS data engineering](aws/INTERVIEW.md) | 5 | [Run/setup](aws/README.md) |
| [Azure data engineering](azure/INTERVIEW.md) | 3 | [Run/setup](azure/README.md) |
| [Google Cloud data engineering](gcp/INTERVIEW.md) | 3 | [Run/setup](gcp/README.md) |
| [Apache Airflow](airflow/INTERVIEW.md) | 4 | [Run/setup](airflow/README.md) |
| [dbt](dbt/INTERVIEW.md) | 4 | [Run/setup](dbt/README.md) |
| [Apache Kafka and streaming](kafka/INTERVIEW.md) | 4 | [Run/setup](kafka/README.md) |
| [Apache Iceberg and open table formats](iceberg/INTERVIEW.md) | 3 | [Run/setup](iceberg/README.md) |
| [PostgreSQL](postgresql/INTERVIEW.md) | 3 | [Run/setup](postgresql/README.md) |
| [DuckDB](duckdb/INTERVIEW.md) | 3 | [Run/setup](duckdb/README.md) |
| [Docker](docker/INTERVIEW.md) | 3 | [Run/setup](docker/README.md) |
| [Terraform](terraform/INTERVIEW.md) | 3 | [Run/setup](terraform/README.md) |
| [Data quality and contracts](data-quality/INTERVIEW.md) | 3 | [Run/setup](data-quality/README.md) |
| [Pipeline observability](observability/INTERVIEW.md) | 3 | [Run/setup](observability/README.md) |
| [Security and governance](security/INTERVIEW.md) | 3 | [Run/setup](security/README.md) |
| [pandas](pandas/INTERVIEW.md) | 3 | [Run/setup](pandas/README.md) |
| [File formats and data layout](file-formats/INTERVIEW.md) | 3 | [Run/setup](file-formats/README.md) |
| [Git and CI/CD for data projects](ci-cd/INTERVIEW.md) | 3 | [Run/setup](ci-cd/README.md) |

## How to revise one topic

1. Read **Understand it** and explain the concept in your own words.
2. Cover **Expected result** and predict the output.
3. Run the example only after satisfying its prerequisites in an appropriate environment.
4. Answer the question aloud in 45–90 seconds: definition, use case, tradeoff, correctness check.
5. Attempt the variation and explain what changes.
6. If you cannot explain the result, repeat the example before memorizing the wording.

Code snippets may depend on the linked lab's schema or intermediate variables. Each example states that dependency. Commented templates are not complete deployed systems.

## If your interview is tomorrow

Use this suggested three-hour revision session; adjust it for the job description.

| Time | Focus | Required outcome |
|---|---|---|
| 0–35 minutes | SQL joins, windows, NULLs, grain | Solve two coding questions and explain row counts. |
| 35–65 minutes | Python and pipeline correctness | Explain retries, stale versions, transaction rollback and memory use. |
| 65–105 minutes | Snowflake or Spark/Databricks, based on the role | Diagnose one performance problem and one incremental-load failure. |
| 105–130 minutes | Airflow, dbt and cloud architecture | Explain logical intervals, dependencies and safe publication. |
| 130–150 minutes | Kafka, CDC, data quality | Explain the sink-commit/offset-commit failure window. |
| 150–180 minutes | Project walkthrough and questions | Give a concise architecture story and answer two follow-ups. |

Do not spend the final hour installing every engine. Use the standard-library local project and focus deeply on technologies named in the role.

## Five scenario questions with answer outlines

### A nightly pipeline doubled yesterday's revenue. Where do you start?

Compare source event count, distinct event IDs, business-key count and destination totals at the same grain. Check retries, repeated appends, duplicated join keys and incomplete latest-version selection. Reproduce with one key. Fix the publication/idempotency design, repair the affected interval and reconcile downstream totals; do not blindly apply DISTINCT.

### A daily job is successful but users report stale data. What does success mean?

Separate task success from source arrival, destination publication and consumer refresh. Inspect source high watermark, logical interval, output manifest/commit and the dashboard refresh/cache. Validate business freshness and completeness rather than relying on the scheduler's green state.

### A Spark job takes much longer after data volume doubles. Would you add executors?

First compare plans, partition sizes, key distributions, shuffle spill, task skew and source file counts. Identify whether one hot key, many tiny tasks, a changed join strategy or driver work dominates. Tune the bottleneck and benchmark on representative data; resource changes alone may not address it.

### How do you backfill 30 days without disturbing today's pipeline?

Define disjoint logical intervals, a shared source-order policy and bounded concurrency. Use separate staging/output identities, coordinate writes to shared keys/partitions, validate each interval and publish atomically or through a manifest. Guard stale updates so historical arrivals cannot regress current state. Track exactly which intervals succeeded.

### An interviewer asks about your project. How do you answer honestly?

Explain work you actually performed, the grain, input/output scale, main failure case and how you verified the result. Use only permitted measurements. For this repository say: “This is a learning project that demonstrates replay-safe ingestion,” rather than claiming it is a production deployment.

## A project answer you can practise

“The learning project receives versioned order events, including duplicate delivery and invalid records. It validates a five-field contract, selects current versions and writes transactional SQLite upserts. Replaying the fixture preserves three orders and 700 cents. Tests cover replay, stale input, conflicts, invalid timestamps and rollback. It deliberately excludes deletes and distributed concurrency; for production I would define source sequence, durable quarantine, checkpoints and operational controls.”

Adapt this wording to your understanding. It describes the repository, not an invented employment achievement.

## Validation and limits

The original local labs were executed in the earlier implementation; see [validation status](VALIDATION.md). The new worked interview exercises were **not executed in this revision**, because the execution environment was unavailable. Markdown/topic coverage and repository publication are checked separately. Use official links in each technology guide and the version-specific documentation for your actual runtime. A comprehensive interview curriculum is larger than this foundation: use the job description to prioritize further topics.

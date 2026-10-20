# pandas

Transform in-memory datasets with explicit dtypes; switch to out-of-core or distributed execution when memory becomes limiting.

[Back to repository index](../README.md)

## Prerequisites and lab

Install a compatible pandas 2.x/3.x in a separate environment if needed. Run `python pandas/transform.py` from repository root. Fixture output is tested locally.

## Topics with worked examples

### Types and missing data

Use nullable dtypes when missing integers are valid. Reject or quarantine invalid records before calculating business totals.

```python
df = pd.read_csv(path, dtype={"order_id":"Int64", "amount_cents":"Int64"})
```

**Check:** Int64 supports missing values, while the lab requires non-missing positive IDs.

### Latest-state deduplication

Sort source versions before keep=last. Without ordering, last only means current input position.

```python
current = valid.sort_values(["updated_at","event_id"]).drop_duplicates("order_id",keep="last")
```

**Check:** Three orders survive. This relies on the canonical timestamp contract and prechecked version conflicts.

### Aggregation and joins

Aggregate at the intended grain and validate expected join cardinality.

```python
dim = pd.DataFrame({"customer_id":[101,102],"segment":["retail","business"]})
result = current.merge(dim,on="customer_id",how="left",validate="many_to_one")
```

**Check:** Three joined rows; duplicate dimension keys raise a MergeError.

## Official references

- https://pandas.pydata.org/docs/user_guide/merging.html
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

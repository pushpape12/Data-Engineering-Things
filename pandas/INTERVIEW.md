# pandas: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Types and missing data
2. Latest-state deduplication
3. Aggregation and joins

## 1. Types and missing data

### Understand it

pandas supports nullable types and multiple missing-value representations. Know whether a missing value means unknown, not applicable or invalid. Vectorized operations and explicit types improve both intent and performance, but object columns and joins can increase memory sharply.

### Practical example

```python
import pandas as pd
s = pd.Series([100,None,250],dtype='Int64')
print(s.sum(),s.isna().sum())
```

**Expected result and reasoning:** Output is 350 and 1. sum skips missing values by default; that behavior may be unacceptable without a completeness check.

### Interview question

**Why can a revenue sum look correct despite missing amounts?**

Aggregation often skips nulls. Count missing amounts explicitly, validate the contract and decide whether partial sums can be published. Do not silently replace all missing values with zero.

**Common mistake:** Treating NaN, empty string and a real zero as equivalent business values.

**Try it yourself:** Show a rule that fails if any required amount is missing.

## 2. Latest-state deduplication

### Understand it

keep='last' refers to the current row ordering, not automatically to latest event time. Sort by a defined source version/tie-breaker and detect incompatible equal-version payloads before collapsing records.

### Practical example

```python
# After loading/validating the shared fixture as in transform.py:
current = valid.sort_values(['updated_at','event_id']).drop_duplicates('order_id',keep='last')
print(current[['order_id','amount_cents']].sort_values('order_id'))
```

**Expected result and reasoning:** Orders 1,2,3 have amounts 150,250,300. Canonical fixture timestamp strings sort chronologically; general formats need parsed timestamps.

### Interview question

**How is drop_duplicates different from groupby?**

drop_duplicates selects rows based on key equality/order policy. groupby aggregates or transforms groups; taking max of each column independently can combine fields from different source rows.

**Common mistake:** Using per-column maxima to construct a latest row with mismatched attributes.

**Try it yourself:** Shuffle input and check that deterministic ordering still gives the same result.

## 3. Aggregation and joins

### Understand it

Validate the expected join cardinality and inspect unmatched keys. pandas merge has NULL-matching behavior that differs from common SQL NULL join semantics, so clean/validate keys deliberately. Business totals must be checked after enrichment.

### Practical example

```python
import pandas as pd
fact = pd.DataFrame({'customer_id':[101,101,102],'amount_cents':[150,300,250]})
dim = pd.DataFrame({'customer_id':[101,102],'segment':['retail','business']})
enriched = fact.merge(dim,on='customer_id',how='left',validate='many_to_one')
print(enriched.groupby('segment')['amount_cents'].sum())
```

**Expected result and reasoning:** retail=450 and business=250. Adding a duplicate customer key to dim makes many_to_one validation fail.

### Interview question

**How do you prevent a merge from silently multiplying rows?**

Validate dimension uniqueness or use merge(validate=...), compare pre/post counts and totals, inspect unmatched keys and define how missing identifiers behave.

**Common mistake:** Assuming pandas NULL keys behave exactly like SQL equality joins.

**Try it yourself:** Add an unmatched customer and report it without dropping the fact row.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

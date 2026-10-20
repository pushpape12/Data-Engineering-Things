# Security and governance: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Least privilege
2. Parameter binding
3. Sensitive data and lineage

## 1. Least privilege

### Understand it

Separate human read access, pipeline write access and administration. Effective access can depend on multiple layers, including database grants, object-store roles and network policies. Use a workload identity scoped to actual tasks.

### Practical example

```text
reader: read curated.orders
transformer: read landing; write sandbox.curated
administrator: manage grants, not the routine job identity
```

**Expected result and reasoning:** A compromised reader should not be able to rewrite landing data or grant new access. The specific syntax depends on the platform.

### Interview question

**How do you troubleshoot a permission failure safely?**

Identify the exact identity, resource and missing operation, inspect effective scoped grants and fix the minimum necessary access. Avoid copying an administrator credential into the pipeline.

**Common mistake:** Granting account-wide owner permissions to make a tutorial run.

**Try it yourself:** Specify permissions for a job that writes one target table but cannot drop its schema.

## 2. Parameter binding

### Understand it

Treat data values separately from SQL syntax. Parameterized execution binds values safely; it usually does not parameterize table or column identifiers. Validate identifiers through a strict allowlist or trusted configuration.

### Practical example

```python
# SQLite example after obtaining a cursor:
order_id = 1
cursor.execute('SELECT amount_cents FROM orders WHERE order_id=?',(order_id,))
```

**Expected result and reasoning:** The bound value is interpreted as data. In the pipeline fixture, order 1 has 150 cents.

### Interview question

**Can I use a placeholder for a table name?**

Most DB-API drivers bind values, not identifiers. Map approved logical names to trusted identifiers or use a driver-supported identifier API. Keep user text out of SQL construction.

**Common mistake:** Replacing quotes manually and calling it SQL injection prevention.

**Try it yourself:** Explain how filtering by a user-supplied customer ID differs from choosing a user-supplied table.

## 3. Sensitive data and lineage

### Understand it

Lineage explains where data came from, how it changed and who owns it; classification governs handling. Avoid copying raw sensitive payloads into public repositories or unrestricted logs. Masking is not a substitute for collecting only necessary data.

### Practical example

```text
source: synthetic orders v1
transform: latest state + reject negative amounts
output: current orders
owner: learning project
classification: public synthetic data
```

**Expected result and reasoning:** A reviewer can trace the derivation without exposing real customer values or private employer details.

### Interview question

**How would you show project experience in an interview?**

Explain architecture, failure modes and measured outcomes you are permitted to discuss. Use synthetic demonstrations and clearly separate hypothetical designs from work you actually performed.

**Common mistake:** Publishing employer code or invented performance claims to strengthen a portfolio.

**Try it yourself:** Draft a sanitized project explanation that contains no internal hostnames or real customer data.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

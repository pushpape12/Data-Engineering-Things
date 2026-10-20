# Git and CI/CD for data projects: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Branches and review
2. Correctness checks
3. CI versus cloud deployment

## 1. Branches and review

### Understand it

A focused branch makes changes reviewable and connects source history to releases. Data code review must include schema/contracts, migration impact, rollback and replay—not just style. Keep generated data and credentials out of public commits.

### Practical example

```bash
git diff --check
git diff --stat
git diff -- README.md python/etl.py
```

**Expected result and reasoning:** These commands show the proposed change, scope and whitespace issues; they do not execute a cloud pipeline or validate business totals.

### Interview question

**What would you review in a data pipeline pull request?**

Source and destination grain, dependency/runtime changes, compatibility, sensitive data handling, replay/backfill behavior, tests and deployment/recovery plan. Evaluate examples against stated prerequisites.

**Common mistake:** Approving a query rewrite solely because it is shorter.

**Try it yourself:** Describe how changing a column type affects downstream consumers.

## 2. Correctness checks

### Understand it

Tests should cover semantic failure modes with expected outputs. A happy-path count is insufficient for duplicate delivery or late updates. Use small controlled fixtures and validate atomic rollback rather than mocking away every meaningful operation.

### Practical example

```bash
python -m unittest discover -s tests -v
```

**Expected result and reasoning:** The existing suite contains five correctness tests. They passed in the earlier implementation; this revision does not claim a new execution while the runtime is unavailable.

### Interview question

**Which tests matter most for incremental ingestion?**

Replay invariance, out-of-order versions, equal-version conflicts, invalid input and transaction failure behavior. Add delete/late-correction tests when those features are implemented.

**Common mistake:** Testing only that a function returns without exceptions.

**Try it yourself:** Create a failing example that appends revenue on every retry, then define the assertion that catches it.

## 3. CI versus cloud deployment

### Understand it

CI runs repeatable checks against changes; deployment alters a running environment. Their credentials and trust boundaries differ. A successful local/static check does not prove a cloud integration or hosted run passed.

### Practical example

```yaml
permissions:
  contents: read
# The existing workflow runs standard-library labs without cloud credentials.
```

**Expected result and reasoning:** Read-only repository permission is enough for these CI checks. The workflow intentionally does not provision cloud resources or run account-bound SQL.

### Interview question

**How would you add a cloud integration test safely?**

Use an isolated environment, scoped short-lived identity, explicit cost/resource limits and deterministic cleanup. Separate untrusted pull-request execution from privileged deployment, and report skipped tests honestly.

**Common mistake:** Passing production secrets to arbitrary PR code or treating skipped tests as passed.

**Try it yourself:** Design deployment gates for a Snowflake schema migration with a rollback plan.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

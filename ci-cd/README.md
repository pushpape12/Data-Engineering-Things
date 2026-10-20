# Git and CI/CD for data projects

Review transformation changes together with contracts and replay behavior before deployment.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

The [GitHub Actions workflow](../.github/workflows/validate.yml) runs on pushes and pull requests. It deliberately does not install Spark, Airflow, dbt or cloud credentials.

## Topics with worked examples

### Branches and review

Use a focused branch and review changes before merging. Keep generated data, secrets and runtime outputs out of Git.

```bash
git diff --check
git diff --stat
```

**Check:** The repository includes .gitignore rules for local data outputs, credentials and infrastructure state.

### Correctness checks

Exercise duplicate delivery, stale events, invalid input and rollback rather than merely asserting imports work.

```bash
python -m unittest discover -s tests -v
```

**Check:** Five tests cover fixture replay, stale events, rollback, timestamp validation and version conflict.

### CI versus cloud deployment

The included workflow compiles optional engine code without importing it, then executes only standard-library labs. Cloud deployment requires separate credentials and approval policy.

```yaml
permissions:
  contents: read
```

**Check:** The workflow cannot publish cloud resources or access application secrets by default.

## Official references

- https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

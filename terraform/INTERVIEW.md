# Terraform: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Variables and validation
2. Plan versus apply
3. State and secrets

## 1. Variables and validation

### Understand it

Variables define configuration inputs; validation constrains acceptable values; locals derive repeated expressions. Outputs expose selected results. These constructs are not cloud resources by themselves.

### Practical example

```hcl
variable "environment" {
  type = string
  default = "sandbox"
}
locals { prefix = "${var.environment}/orders" }
output "prefix" { value = local.prefix }
```

**Expected result and reasoning:** For the default, output is sandbox/orders after evaluation. The bundled main.tf also validates allowed environment names.

### Interview question

**Variables versus locals: what is the difference?**

Variables are caller-controlled inputs, while locals name expressions internal to the module. Use variables for intended configuration flexibility and locals for derived values/reuse.

**Common mistake:** Exposing every internal implementation detail as an input.

**Try it yourself:** Add a region input and identify which values should be constrained.

## 2. Plan versus apply

### Understand it

init prepares configuration dependencies/backend; validate checks configuration consistency; plan compares desired configuration with observed/state information; apply performs approved changes. A plan is not a promise the world cannot change before apply.

### Practical example

```bash
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

**Expected result and reasoning:** The bundled configuration declares no provider/resources and proposes a landing_prefix output of sandbox/orders/raw/. Commands require Terraform; not executed here.

### Interview question

**What would you review before applying an infrastructure change?**

Resource additions/replacements/deletions, privilege exposure, state/workspace/region, provider versions and expected cost. Coordinate review with the plan being applied and replan if assumptions change.

**Common mistake:** Treating plan or validate as a production deployment test.

**Try it yourself:** Explain how applying to the wrong workspace can affect the wrong resources.

## 3. State and secrets

### Understand it

State maps configuration addresses to managed objects and may contain sensitive values. Protect its backend, history and concurrency. Marking an output sensitive limits display but does not make underlying state harmless.

### Practical example

```text
Git: reviewed configuration
secure backend: state, access control, recovery history
runtime secret store: application credentials
```

**Expected result and reasoning:** State and plan artifacts should not be committed to this public repository. Backend locking semantics depend on the configured system.

### Interview question

**Why not store Terraform state in a public Git repository?**

It can disclose resource details and secrets, creates poor concurrency control and complicates safe operations. Use an approved backend with encryption/access controls and coordinated locking/recovery.

**Common mistake:** Assuming sensitive=true encrypts or removes the secret from state.

**Try it yourself:** Design how two engineers avoid concurrent conflicting applies.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.

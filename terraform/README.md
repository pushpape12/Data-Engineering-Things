# Terraform

Model infrastructure inputs and review plans before any resource change.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Optional Terraform 1.5+ (<2.0) CLI lab; not executed here. No infrastructure resources are declared.

## Topics with worked examples

### Variables and validation

Validate environment names early and construct predictable data prefixes.

```hcl
variable "environment" {
  type = string
  default = "sandbox"
}
```

**Check:** The complete main.tf restricts environment to sandbox/dev/prod.

### Plan versus apply

The bundled configuration has no providers or resources, so it illustrates evaluation without provisioning cloud infrastructure.

```bash
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

**Check:** Expected landing_prefix output: sandbox/orders/raw/. Do not run apply for this lesson.

### State and secrets

State can contain sensitive values. Use an access-controlled encrypted remote backend for real projects, and never commit state or secret variable files.

```text
source control: reviewed configuration
secure backend: state + locking where supported
secret manager: runtime credentials
```

**Check:** Plan files may also contain secrets; do not publish them.

## Official references

- https://developer.hashicorp.com/terraform/language
- https://developer.hashicorp.com/terraform/language/state/sensitive-data

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).

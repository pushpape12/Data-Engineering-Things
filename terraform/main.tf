terraform {
  required_version = ">= 1.5, < 2.0"
}
variable "environment" {
  type    = string
  default = "sandbox"
  validation {
    condition     = contains(["sandbox", "dev", "prod"], var.environment)
    error_message = "Use sandbox, dev or prod."
  }
}
variable "dataset" {
  type    = string
  default = "orders"
}
locals {
  prefix = "${var.environment}/${var.dataset}"
}
output "landing_prefix" {
  value = "${local.prefix}/raw/"
}

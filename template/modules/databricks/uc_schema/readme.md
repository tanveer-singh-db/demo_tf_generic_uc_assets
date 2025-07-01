# 📦 Databricks Unity Catalog Schema Terraform Module

This Terraform module provisions a Unity Catalog **schema** inside a given **catalog** using the [Databricks Terraform Provider](https://registry.terraform.io/providers/databricks/databricks/latest).

---

## ✅ Features

- Creates a Unity Catalog schema (`databricks_schema`).
- Supports dependency injection on the parent catalog.
- Uses aliased providers for multi-environment flexibility.

---

## 🚀 Usage

```hcl
provider "databricks" {
  alias       = "azure"
  host        = var.databricks_workspace_url
  azure_auth  = true
}

module "schema" {
  source       = "./modules/schema"
  name         = "silver"
  catalog_name = module.catalog.catalog_name
  comment      = "Managed by TF"

  depends_on = [module.catalog]

  providers = {
    databricks = databricks.azure
  }
}
```

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_databricks"></a> [databricks](#requirement\_databricks) | >= 1.48.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_databricks"></a> [databricks](#provider\_databricks) | >= 1.48.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_schema.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/schema) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_schema"></a> [schema](#input\_schema) | Configuration for a Databricks schema | <pre>object({<br/>    name                         = string<br/>    catalog_name                 = string<br/>    storage_root                 = optional(string)<br/>    owner                        = optional(string)<br/>    comment                      = optional(string)<br/>    properties                   = optional(map(string))<br/>    enable_predictive_optimization = optional(string, "INHERIT")<br/>    force_destroy                = optional(bool, false)<br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_schema_name"></a> [schema\_name](#output\_schema\_name) | The name of the created schema |
<!-- END_TF_DOCS -->
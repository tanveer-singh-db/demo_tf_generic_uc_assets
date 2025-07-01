# 📦 Databricks Unity Catalog - Terraform Module

This Terraform module provisions a [Databricks Unity Catalog](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/catalog) on Azure with a defined storage root and optional ownership.

---

## ✅ Features

- Creates a Databricks Unity Catalog using `databricks_catalog`.
- Accepts a storage root path in ADLS Gen2.
- Supports optional `owner` (user or group).
- Supports dependency injection (e.g., depends on external location).
- Uses aliased Databricks providers (e.g., `databricks.azure`).

---

## 🚀 Usage

> ✅ Ensure the aliased `databricks` provider is defined and passed in the root module.

```hcl
provider "databricks" {
  alias       = "workspace"
  host        = var.databricks_workspace_url
  azure_auth  = true
}

module "catalog" {
  source = "./modules/catalog"

  name         = "demo_ts_catalog_1"
  comment      = "Catalog created by Terraform"
  storage_root = local.catalog_base_url
  owner        = "tanveer@databricks.com"

  # depends_on = [module.external_location]

  providers = {
    databricks = databricks.workspace
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
| [databricks_catalog.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/catalog) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_catalog"></a> [catalog](#input\_catalog) | Configuration for a single catalog | <pre>object({<br/>    name                         = string<br/>    storage_root                 = optional(string)<br/>    provider_name                = optional(string)<br/>    share_name                   = optional(string)<br/>    connection_name              = optional(string)<br/>    owner                        = optional(string)<br/>    isolation_mode               = optional(string, "ISOLATED")<br/>    enable_predictive_optimization = optional(string, "INHERIT")<br/>    comment                      = optional(string)<br/>    properties                   = optional(map(string))<br/>    options                      = optional(map(string))<br/>    force_destroy                = optional(bool, false)<br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_catalog_name"></a> [catalog\_name](#output\_catalog\_name) | The name of the created catalog |
<!-- END_TF_DOCS -->
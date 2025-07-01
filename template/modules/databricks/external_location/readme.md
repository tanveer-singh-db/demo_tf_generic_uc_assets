# 📦 Databricks External Location Terraform Module (Azure)

This Terraform module provisions a [Databricks External Location](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/external_location) on Azure, using a Databricks Storage Credential backed by an Azure Access Connector.

It allows Unity Catalog to securely access a path in ADLS Gen2 (e.g., `abfss://container@account.dfs.core.windows.net/`).

---
##  Features

- Creates a `databricks_external_location` resource for Unity Catalog.
- References an existing Databricks `storage_credential`.
- Accepts a fully-qualified URL to an ADLS Gen2 location.

---

##   Usage

> Ensure the `databricks_storage_credential` has already been created, and the `databricks` provider is defined in your root module.

```hcl
provider "databricks" {
  alias       = "workspace"
  host        = var.databricks_workspace_url
  azure_auth  = true
}

module "external_location" {
  source = "./modules/external_location"

  name            = "${local.container_name}@${local.storage_account_name}"
  url             = local.catalog_base_url
  comment         = "External location for Unity Catalog"
  credential_name = module.storage_credential.storage_credential_name

  depends_on = [module.storage_credential]

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
| [databricks_external_location.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/external_location) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_external_location"></a> [external\_location](#input\_external\_location) | Configuration for Azure external location | <pre>object({<br/>    name               = string<br/>    url                = string       # Azure format: abfss://<container>@<storage_account>.dfs.core.windows.net/<path><br/>    credential_name    = string<br/>    owner              = optional(string)<br/>    comment            = optional(string)<br/>    skip_validation    = optional(bool, false)<br/>    fallback           = optional(bool, false)<br/>    read_only          = optional(bool, false)<br/>    force_destroy      = optional(bool, false)<br/>    force_update       = optional(bool, false)<br/>    isolation_mode     = optional(string, "ISOLATION_MODE_ISOLATED")<br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_external_location_name"></a> [external\_location\_name](#output\_external\_location\_name) | n/a |
<!-- END_TF_DOCS -->
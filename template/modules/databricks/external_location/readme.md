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


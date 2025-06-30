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

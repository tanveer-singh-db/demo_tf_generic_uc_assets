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

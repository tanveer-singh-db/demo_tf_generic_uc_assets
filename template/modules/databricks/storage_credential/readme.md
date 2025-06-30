# 📦 Databricks Storage Credential Terraform Module (Azure)

This Terraform module provisions a [Databricks Unity Catalog Storage Credential](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/storage_credential) using an **Azure Access Connector with a System Assigned Managed Identity**.

It is intended for use with Unity Catalog to allow secure access to Azure Data Lake Storage (ADLS Gen2) accounts.

---

## ✅ Features

- Creates a `databricks_storage_credential` backed by an Azure **access connector** (managed identity).
- Works with **aliased Databricks providers** (e.g. `databricks.azure`).
- Cleanly separates provider configuration from the module (via `providers` block).

---

## 🚀 Usage

> 📌 Ensure you’ve created a Databricks Access Connector and configured an aliased Databricks provider (see below).

```hcl
provider "databricks" {
  alias       = "azure"
  host        = var.databricks_workspace_url
  azure_auth  = true
}

module "storage_credential" {
  source = "./modules/storage_credential"

  name                = "demo_storage_credential"
  comment             = "Storage credential for Unity Catalog"
  access_connector_id = module.databricks_access_connector.access_connector_id

  providers = {
    databricks = databricks.workspace
  }
}
```
## 📥 Input Variables

| Name                  | Type   | Description                                                     | Required                                     |
| --------------------- | ------ | --------------------------------------------------------------- | -------------------------------------------- |
| `name`                | string | Name of the storage credential in Databricks.                   | ✅ Yes                                        |
| `comment`             | string | Optional comment for documentation purposes.                    | ❌ No (default: `"Provisioned by Terraform"`) |
| `access_connector_id` | string | Azure resource ID of the `azurerm_databricks_access_connector`. | ✅ Yes                                        |

## 📤 Output Variables

| Name                      | Description                                |
| ------------------------- | ------------------------------------------ |
| `storage_credential_id`   | ID of the Databricks storage credential.   |
| `storage_credential_name` | Name of the Databricks storage credential. |



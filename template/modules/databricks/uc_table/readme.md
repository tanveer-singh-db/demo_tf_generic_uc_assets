# 📦 Databricks SQL Table Terraform Module

This module provisions one or more Unity Catalog SQL tables using the [`databricks_sql_table`](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/sql_table) resource, with support for MANAGED, EXTERNAL, and VIEW types.

---

## ✅ Features

- Supports `MANAGED`, `EXTERNAL`, and `VIEW` table types.
- Supports optional clustering, partitioning, data source format, and view definitions.
- Supports detailed column definitions with optional identity, nullable, and comments.
- Supports assigning `owner` and custom `options` and `properties`.
- Handles multiple tables using `for_each`.

---

## 🚀 Usage

```hcl
locals {
  sql_tables = [
    {
      name         = "sales_fact"
      catalog_name = "demo_ts_catalog_1"
      schema_name  = "silver"
      table_type   = "MANAGED"
      comment      = "Fact sales table"
      cluster_keys = ["region_id"]
      # partitions   = ["sale_date"] -- Note partitions and cluster_keys are mutually exclusive
      data_source_format = "delta"
      columns = [
        { name = "id", type = "bigint", nullable = false, identity = "always" },
        { name = "region_id", type = "int" },
        { name = "sale_date", type = "date" }
      ]
    },
    {
      name             = "active_users_view"
      catalog_name     = "demo_ts_catalog_1"
      schema_name      = "silver"
      table_type       = "VIEW"
      view_definition  = "SELECT * FROM users WHERE active = true"
      comment          = "View of active users"
    }
  ]
}

module "sql_tables" {
  source     = "./modules/sql_table"
  sql_tables = local.sql_tables
  depends_on = [module.schema]

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
| [databricks_sql_endpoint.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/sql_endpoint) | resource |
| [databricks_sql_table.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/sql_table) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_sql_tables"></a> [sql\_tables](#input\_sql\_tables) | List of SQL table definitions, each a map with keys like name, catalog\_name, schema\_name, etc. | <pre>list(object({<br/>    name               = string<br/>    catalog_name       = string<br/>    schema_name        = string<br/>    table_type         = string<br/>    comment            = optional(string)<br/>    owner              = optional(string)<br/>    view_definition    = optional(string)<br/>    cluster_keys       = optional(list(string))<br/>    partitions         = optional(list(string))<br/>    data_source_format = optional(string)<br/>    storage_location   = optional(string)<br/>    options            = optional(map(string))<br/>    properties         = optional(map(string))<br/>    columns = optional(list(object({<br/>      name     = string<br/>      type     = optional(string, "string")<br/>      comment  = optional(string)<br/>      nullable = optional(bool, true)<br/>      identity = optional(string) # only "default" or "always"<br/>    })))<br/>  }))</pre> | `[]` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
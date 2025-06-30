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

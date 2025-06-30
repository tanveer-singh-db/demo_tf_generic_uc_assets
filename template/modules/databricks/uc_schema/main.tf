resource "databricks_schema" "this" {
  name        = var.schema.name
  catalog_name = var.schema.catalog_name
  storage_root = var.schema.storage_root
  owner        = var.schema.owner
  comment      = var.schema.comment
  properties   = var.schema.properties
  enable_predictive_optimization = var.schema.enable_predictive_optimization
  force_destroy = var.schema.force_destroy
}
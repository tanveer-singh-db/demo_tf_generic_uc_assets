resource "databricks_catalog" "this" {
  name        = var.catalog.name
  storage_root = var.catalog.storage_root
  provider_name = var.catalog.provider_name
  share_name    = var.catalog.share_name
  connection_name = var.catalog.connection_name
  owner        = var.catalog.owner
  isolation_mode = var.catalog.isolation_mode
  enable_predictive_optimization = var.catalog.enable_predictive_optimization
  comment      = var.catalog.comment
  properties   = var.catalog.properties
  options      = var.catalog.options
  force_destroy = var.catalog.force_destroy
}
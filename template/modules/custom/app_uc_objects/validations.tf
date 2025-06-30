
# data "databricks_catalogs" "all" {}
#
# # Get details for all existing catalogs
# data "databricks_catalog" "existing" {
#   for_each = toset(data.databricks_catalogs.all.ids)
#   name     = each.key
# }
#
# locals {
#   existing_storage_roots = {
#     for catalog in data.databricks_catalogs.all.catalogs :
#     catalog.storage_root => catalog.name
#     if catalog.storage_root != null
#   }
#
#   defined_storage_roots = [
#     for catalog in local.catalogs : catalog.storage_root
#     if catalog.storage_root != null
#   ]
#
#   storage_root_counts = {
#     for root in local.defined_storage_roots :
#     root => length([for r in local.defined_storage_roots : r if r == root])
#   }
#
#   duplicate_storage_roots = {
#     for root, count in local.storage_root_counts :
#     root => count
#     if count > 1
#   }
#
#   # duplicate_existing_storage_root = {
#   #   for roo
#   # }
#
#   has_duplicate_configured_storage_root = length(local.duplicate_storage_roots) > 0
#
#
#
# }
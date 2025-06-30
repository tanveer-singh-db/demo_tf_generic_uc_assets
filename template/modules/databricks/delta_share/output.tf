output "recipient_ids" {
  value = { for k, v in databricks_recipient.this : k => v.id }
}

output "share_ids" {
  value = { for k, v in databricks_share.this : k => v.id }
}



# output "catalogs_to_create_debug" {
#   value = local.catalogs_to_create
# }

# output "catalog_names" {
#   value = [for k, v in databricks_catalog.this : v.name]
# }

# output "current_metastore_id" {
#   value = data.databricks_current_metastore.current.metastore_info
# }



resource "databricks_storage_credential" "this" {
  name           = var.storage_credential.name
  comment        = var.storage_credential.comment
  metastore_id   = var.storage_credential.metastore_id
  owner          = var.storage_credential.owner
  read_only      = var.storage_credential.read_only
  skip_validation = var.storage_credential.skip_validation
  force_destroy  = var.storage_credential.force_destroy
  force_update   = var.storage_credential.force_update
  isolation_mode = var.storage_credential.isolation_mode

  azure_managed_identity {
    access_connector_id = var.storage_credential.access_connector_id
  }

}
#
# # Warning resource for plan-time notifications
# resource "terraform_data" "isolation_warning" {
#   # Always run this resource
#   input = var.storage_credential.isolation_mode
#
#   # lifecycle {
#   #   # Show warning even if no changes are being made
#   #   replace_triggered_by = [input]
#   # }
# }


# Get current workspace metastore ID
data "databricks_current_metastore" "current" {}

# Create recipients
resource "databricks_recipient" "this" {
  for_each = var.delta_sharing_config.recipients == null ? {} : { for r in var.delta_sharing_config.recipients : r.name => r }

  name               = each.value.name
  authentication_type = "DATABRICKS"
  comment            = each.value.comment
  data_recipient_global_metastore_id = each.value.recipient_sharing_id
}

# Create shares with their objects
resource "databricks_share" "this" {
  for_each = local.shares_with_objects == null ? {} : local.shares_with_objects

  name    = each.value.name
  comment = each.value.comment

  dynamic "object" {
    for_each = each.value.objects
    content {
      name = object.value.name
      data_object_type = object.value.type
      history_data_sharing_status = object.value.history_data_sharing_status
    }
  }
  depends_on = [databricks_recipient.this]
}

# Grant share access to recipients
resource "databricks_grant" "share_grant" {
  for_each = local.shares_with_objects == null ? {} : local.shares_with_objects
  share = each.value.name
  principal  = each.value.recipient_name
  privileges = ["SELECT"]

  depends_on = [databricks_share.this]
}

# # Create catalogs only when metastore IDs match
# resource "databricks_catalog" "this" {
#   for_each = local.catalogs_to_create == null ? {} : local.catalogs_to_create
#   name        = each.value.recipient_catalog_name
#   provider_name = local.current_global_metastore_id
#   share_name = each.value.share_name
#
#   depends_on = [ databricks_grant.share_grant ]
# }
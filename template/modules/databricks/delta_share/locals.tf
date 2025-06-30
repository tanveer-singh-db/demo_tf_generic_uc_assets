
locals {

  # current_global_metastore_id = data.databricks_current_metastore.current.metastore_info[0].global_metastore_id

  # Create recipient metastore ID map
  recipient_metastore_map = var.delta_sharing_config.recipients == null ? {} : {
    for r in var.delta_sharing_config.recipients : r.name => r.recipient_sharing_id
  }

  # # Identify catalogs to create (only when recipient metastore matches current)
  # catalogs_to_create = distinct(flatten([
  #   for share in var.delta_sharing_config.shares : [
  #     share.recipient_catalog_name != null &&
  #     local.recipient_metastore_map[share.recipient_name] == data.databricks_current_metastore.current.metastore_info[0].global_metastore_id ?
  #     [share.recipient_catalog_name] : []
  #   ]
  # ]))

  catalogs_to_create = var.delta_sharing_config.shares == null ? {} : {
    for share in var.delta_sharing_config.shares :
    share.internal_recipient_catalog_name => {
      recipient_catalog_name = share.internal_recipient_catalog_name
      share_name             = share.name
    }
          if share.internal_recipient_catalog_name != null
    # if share.internal_recipient_catalog_name != null && data.databricks_current_metastore.current.metastore_info &&
    #    local.recipient_metastore_map[share.recipient_name] == data.databricks_current_metastore.current.metastore_info[0].global_metastore_id
  }


  # Prepare shares with objects
  shares_with_objects = var.delta_sharing_config.shares == null ? {} : {
    for s in var.delta_sharing_config.shares : s.name => s
  }
}

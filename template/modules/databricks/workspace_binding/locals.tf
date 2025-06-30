locals {
  # Flatten all bindings into distinct resource configurations
  all_bindings = flatten([
    for wb in var.workspace_bindings : [
      # Process catalogs
      [
        for catalog in wb.catalogs : {
          workspace_id   = wb.workspace_id
          securable_name = catalog
          securable_type = "catalog"
          binding_type   = wb.binding_type
        }
      ],
      # Process external locations
      [
        for location in wb.external_locations : {
          workspace_id   = wb.workspace_id
          securable_name = location
          securable_type = "external_location"
          binding_type   = "BINDING_TYPE_READ_WRITE"
        }
      ],
      # Process storage credentials
      [
        for credential in wb.storage_credentials : {
          workspace_id   = wb.workspace_id
          securable_name = credential
          securable_type = "storage_credential"
          binding_type   = wb.binding_type
        }
      ],
      # Process credentials
      [
        for credential in wb.credentials : {
          workspace_id   = wb.workspace_id
          securable_name = credential
          securable_type = "storage_credential"
          binding_type   = wb.binding_type
        }
      ]
    ]
  ])

  # Convert to map with unique keys for resource for_each
  bindings_map = {
    for binding in local.all_bindings :
    "${binding.workspace_id}|${binding.securable_type}|${binding.securable_name}" => binding
  }
}



#
# locals {
#  # flattened_bindings = flatten([
#  #    for wb in var.workspace_bindings : [
#  #      for catalog in wb.catalogs : {
#  #        workspace_id = wb.workspace_id
#  #        catalog       = catalog
#  #        securable_type = 'catalog'
#  #        # workspace_url = wb.workspace_url
#  #        key           = "${wb.workspace_id}:${catalog}"
#  #      }
#  #    ]
#  #  ])
#   # Flatten all bindings into distinct resource configurations
#   all_bindings = flatten([
#     for wb in var.workspace_bindings : [
#       # Process catalogs
#       for catalog in wb.catalogs : {
#         workspace_id   = wb.workspace_id
#         securable_name = catalog
#         securable_type = "catalog"
#         binding_type   = wb.binding_type
#       },
#       # Process external locations
#       for location in wb.external_locations : {
#         workspace_id   = wb.workspace_id
#         securable_name = location
#         securable_type = "external_location"
#         binding_type   = wb.binding_type
#       },
#       # Process storage credentials
#       for credential in wb.storage_credentials : {
#         workspace_id   = wb.workspace_id
#         securable_name = credential
#         securable_type = "storage_credential"
#         binding_type   = wb.binding_type
#       }
#     ]
#   ])
#
#   # Convert to map with unique keys for resource for_each
#   bindings_map = {
#     for binding in local.all_bindings :
#     "${binding.workspace_id}|${binding.securable_type}|${binding.securable_name}" => binding
#   }
# }
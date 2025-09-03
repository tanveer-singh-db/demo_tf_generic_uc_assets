#
# Workspace Binding Transformation Logic
#
# This module transforms workspace binding configurations into individual resource bindings.
# Each workspace can bind to multiple types of securables (catalogs, external_locations, storage_credentials).
# The configuration supports a many-to-many relationship between workspaces and securables.
#

locals {
  # Transform nested workspace binding configuration into flat list of individual bindings
  # This allows for efficient resource creation using for_each loops
  all_bindings = flatten([
    for wb in var.workspace_bindings : [
      # Bind catalogs to workspace
      # Each catalog gets bound individually with the specified binding type
      [
        for catalog in wb.catalogs : {
          workspace_id   = wb.workspace_id
          securable_name = catalog
          securable_type = "catalog"
          binding_type   = wb.binding_type
        }
      ],
      # Bind external locations to workspace
      # External locations default to READ_WRITE binding type for data access
      [
        for location in wb.external_locations : {
          workspace_id   = wb.workspace_id
          securable_name = location
          securable_type = "external_location"
          binding_type   = "BINDING_TYPE_READ_WRITE"
        }
      ],
      # Bind storage credentials to workspace (modern format)
      # Storage credentials enable access to external storage systems
      [
        for credential in wb.storage_credentials : {
          workspace_id   = wb.workspace_id
          securable_name = credential
          securable_type = "storage_credential"
          binding_type   = wb.binding_type
        }
      ],
      # Bind credentials to workspace (legacy format for backwards compatibility)
      # Maps to storage_credential securable type
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

  # Create unique resource map for Terraform for_each
  # Key format: "{workspace_id}|{securable_type}|{securable_name}"
  # This ensures each binding is unique and prevents resource conflicts
  bindings_map = {
    for binding in local.all_bindings :
    "${binding.workspace_id}|${binding.securable_type}|${binding.securable_name}" => binding
  }
}

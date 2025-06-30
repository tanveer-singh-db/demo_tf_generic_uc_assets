

# # Look up the workspace using the host
# data "databricks_workspaces" "all" {
#   provider = databricks.account
# }




resource "databricks_workspace_binding" "this" {
  for_each = local.bindings_map
  workspace_id   = each.value.workspace_id
  securable_name = each.value.securable_name
  securable_type = each.value.securable_type
  binding_type   = each.value.binding_type
}

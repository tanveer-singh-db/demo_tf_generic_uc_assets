# Lookup account-level groups
data "databricks_group" "account_groups" {
  for_each     = local.groups == null ? {} : { for group in local.groups : group.name => group }
  display_name = each.key
  provider     = databricks.account
}

resource "databricks_permission_assignment" "group_assignments" {
  for_each = {
    for group in local.groups :
    group.name => {
      id          = data.databricks_group.account_groups[group.name].id
      permissions = group.permissions
    }
  }
  principal_id = each.value.id
  permissions  = each.value.permissions
  provider     = databricks.workspace
  depends_on = [data.databricks_group.account_groups]
}

data "databricks_user" "admin_users" {
  for_each = toset(local.admin_users)
  user_name = each.value
  provider = databricks.account
}

resource "databricks_permission_assignment" "admin_user_assignments" {
  for_each     = data.databricks_user.admin_users
  principal_id = each.value.id
  permissions  = ["ADMIN"]
  provider     = databricks.workspace
}

data "databricks_user" "users" {
  for_each = toset(local.users)
  user_name = each.value
  provider = databricks.account
}

resource "databricks_permission_assignment" "user_assignments" {
  for_each     = data.databricks_user.users
  principal_id = each.value.id
  permissions  = ["USER"]
  provider     = databricks.workspace
}


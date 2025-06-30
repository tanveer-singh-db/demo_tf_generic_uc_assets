locals{
  groups = coalesce(try(var.workspace_onboarding_config.groups,[]),[])
  users = coalesce(try(var.workspace_onboarding_config.users, []),[])
  admin_users = coalesce(try(var.workspace_onboarding_config.admin_users, []),[])
}

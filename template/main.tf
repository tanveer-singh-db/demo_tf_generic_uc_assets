
# create unity catalog objects
module "app_uc_objects" {
  source            = "./modules/custom/app_uc_objects"
  uc_objects_config = local.uc_object_config
  providers = {
    databricks = databricks.workspace
  }
  # depends_on = [module.workspace_onboarding]
}

# create delta sharing objects
module "delta_sharing" {
  source = "./modules/databricks/delta_share"
  delta_sharing_config = local.delta_sharing_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.app_uc_objects]
}

# apply grants
module "uc_grants" {
  source               = "./modules/databricks/grants"
  unity_catalog_grants = local.uc_object_grants_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.delta_sharing]
}

module "workspace_bindings" {
  source             = "./modules/databricks/workspace_binding"
  workspace_bindings = local.workspace_bindings_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.uc_grants]
}

#
# Unity Catalog Deployment Orchestration
#
# This configuration orchestrates the creation of Unity Catalog resources in a specific sequence
# to ensure proper dependencies and resource relationships are maintained.
# All modules execute against the workspace-specific Databricks provider.
#

# Step 1: Create core Unity Catalog objects (catalogs, schemas, tables, external locations)
module "app_uc_objects" {
  source            = "./modules/custom/app_uc_objects"
  uc_objects_config = local.uc_object_config
  providers = {
    databricks = databricks.workspace
  }
}

# Step 2: Create Delta Sharing objects (recipients and shares)
module "delta_sharing" {
  source               = "./modules/databricks/delta_share"
  delta_sharing_config = local.delta_sharing_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.app_uc_objects]
}

# Step 3: Apply access grants and permissions
module "uc_grants" {
  source               = "./modules/databricks/grants"
  unity_catalog_grants = local.uc_object_grants_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.delta_sharing]
}

# Step 4: Configure workspace bindings
# Links catalogs and external locations to specific workspaces
module "workspace_bindings" {
  source             = "./modules/databricks/workspace_binding"
  workspace_bindings = local.workspace_bindings_config
  providers = {
    databricks = databricks.workspace
  }
  depends_on = [module.uc_grants]
}
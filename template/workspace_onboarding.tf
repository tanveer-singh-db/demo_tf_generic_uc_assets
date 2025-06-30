#
# locals {
#   workspace_onboarding_config = yamldecode(file("${local.config_base_path}/workspace_onboarding.yml"))
# }
#
# module "workspace_onboarding" {
#   source                      = "./modules/custom/app_onboard_workspace_groups"
#   workspace_onboarding_config = local.workspace_onboarding_config
#   providers = {
#     databricks.account   = databricks.account
#     databricks.workspace = databricks.workspace
#   }
# }

variable "cloudEnvironment" {
  type        = string
  description = "Cloud Environment Name for Config"
}

variable "region" {
  type        = string
  description = "Name of the region"
}

variable "workspaceInfo" {
  type        = string
  description = "Workspace Identifier for config"
}

# variable "deployment_subscription_id" {
#   type        = string
#   description = "Subscription ID to be used for the deployment"
# }
variable "deployment_tenant_id" {
  type        = string
  description = "Subscription ID to be used for the deployment"
}
variable "databricks_workspace_url" {
  type        = string
  description = "Databricks workspace url"
}
variable "client_id" {
  type        = string
  description = "Azure service principal client ID"
}

variable "client_secret" {
  type        = string
  description = "Azure service principal client secret"
  sensitive   = true
}

#
# variable "uc_objects_config_file" {
#   type        = string
#   description = "Config file for creating Unity Catalog Objects"
# }

# variable "uc_object_grants_config_file" {
#   type        = string
#   description = "Config file for creating Unity Catalog Object Grants"
# }
# variable "workspace_binding_config_file" {
#   type        = string
#   description = "Config file for creating Unity Catalog Object Grants"
# }
# variable "delta_sharing_config_file" {
#   type        = string
#   description = "Config file for creating Unity Catalog Object Grants"
# }
# variable "databricks_account_id" {
#   type        = string
#   description = "Databricks account id"
# }

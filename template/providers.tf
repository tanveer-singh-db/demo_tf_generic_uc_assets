terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.48.2"
    }
  }
}

provider "databricks" {
  alias = "workspace"
  auth_type = "azure-client-secret"
  host  = var.databricks_workspace_url
  azure_client_id             = var.client_id
  azure_client_secret         = var.client_secret
  azure_tenant_id = var.deployment_tenant_id

}

# provider "databricks" {
#   alias           = "account"
#   host            = "https://accounts.azuredatabricks.net"
#   account_id      = var.databricks_account_id
#   azure_tenant_id = var.deployment_tenant_id
# }


terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.48.2"
      # configuration_aliases = [
      #   databricks.account,
      #   databricks.workspace
      # ]
    }
  }
}

# Tell Terraform this module expects these two provider aliases
provider "databricks" {
  alias = "account"
}

provider "databricks" {
  alias = "workspace"
}
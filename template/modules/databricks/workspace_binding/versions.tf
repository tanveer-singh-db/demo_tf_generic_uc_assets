terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.48.2"
      # configuration_aliases = [
      #   databricks.account
      # ]
    }
  }
}

# # Tell Terraform this module expects these two provider aliases
# provider "databricks" {
#   alias = "account"
# }

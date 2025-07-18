
## 🛠️ Provider Configuration & Aliasing
This module does not hardcode the provider inside. Instead, it expects the caller (root module) to:

Configure the databricks provider using an alias (e.g., databricks.azure).

Pass it to the module using the providers argument.

### ✅ Root module should define:
```hcl
provider "databricks" {
  alias      = "workspace"
  host       = var.databricks_workspace_url
  azure_auth = true
}
```
### ✅ And call the module with:
```hcl
providers = {
  databricks = databricks.workspace
}
```
<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

No providers.

## Modules

No modules.

## Resources

No resources.

## Inputs

No inputs.

## Outputs

No outputs.
<!-- END_TF_DOCS -->
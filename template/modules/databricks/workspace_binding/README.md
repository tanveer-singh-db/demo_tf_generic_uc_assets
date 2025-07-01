<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_databricks"></a> [databricks](#requirement\_databricks) | >= 1.48.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_databricks"></a> [databricks](#provider\_databricks) | >= 1.48.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_workspace_binding.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_workspace_bindings"></a> [workspace\_bindings](#input\_workspace\_bindings) | List of bindings, each workspace\_URL, and catalogs | <pre>list(object({<br/>    workspace_id = string<br/>    # workspace_url = string<br/>    catalogs      = optional(list(string),[])<br/>    external_locations = optional(list(string),[])<br/>    storage_credentials = optional(list(string),[])<br/>    credentials = optional(list(string),[])<br/>    binding_type = optional(string, "BINDING_TYPE_READ_ONLY")<br/>  }))</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_bindings"></a> [bindings](#output\_bindings) | n/a |
<!-- END_TF_DOCS -->
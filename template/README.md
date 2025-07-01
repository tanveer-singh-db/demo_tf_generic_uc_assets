<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_databricks"></a> [databricks](#requirement\_databricks) | >= 1.48.2 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_app_uc_objects"></a> [app\_uc\_objects](#module\_app\_uc\_objects) | ./modules/custom/app_uc_objects | n/a |
| <a name="module_delta_sharing"></a> [delta\_sharing](#module\_delta\_sharing) | ./modules/databricks/delta_share | n/a |
| <a name="module_uc_grants"></a> [uc\_grants](#module\_uc\_grants) | ./modules/databricks/grants | n/a |
| <a name="module_workspace_bindings"></a> [workspace\_bindings](#module\_workspace\_bindings) | ./modules/databricks/workspace_binding | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_client_id"></a> [client\_id](#input\_client\_id) | Azure service principal client ID | `string` | n/a | yes |
| <a name="input_client_secret"></a> [client\_secret](#input\_client\_secret) | Azure service principal client secret | `string` | n/a | yes |
| <a name="input_cloudEnvironment"></a> [cloudEnvironment](#input\_cloudEnvironment) | Cloud Environment Name for Config | `string` | n/a | yes |
| <a name="input_databricks_workspace_url"></a> [databricks\_workspace\_url](#input\_databricks\_workspace\_url) | Databricks workspace url | `string` | n/a | yes |
| <a name="input_deployment_tenant_id"></a> [deployment\_tenant\_id](#input\_deployment\_tenant\_id) | Subscription ID to be used for the deployment | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Name of the region | `string` | n/a | yes |
| <a name="input_workspaceInfo"></a> [workspaceInfo](#input\_workspaceInfo) | Workspace Identifier for config | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_debug_config_base_path"></a> [debug\_config\_base\_path](#output\_debug\_config\_base\_path) | n/a |
| <a name="output_debug_merged_config"></a> [debug\_merged\_config](#output\_debug\_merged\_config) | n/a |
| <a name="output_debug_uc_object_config"></a> [debug\_uc\_object\_config](#output\_debug\_uc\_object\_config) | n/a |
| <a name="output_external_locations"></a> [external\_locations](#output\_external\_locations) | n/a |
| <a name="output_planned_external_locations"></a> [planned\_external\_locations](#output\_planned\_external\_locations) | n/a |
<!-- END_TF_DOCS -->
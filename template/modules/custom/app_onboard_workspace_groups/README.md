<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_databricks"></a> [databricks](#requirement\_databricks) | >= 1.48.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_databricks.account"></a> [databricks.account](#provider\_databricks.account) | >= 1.48.2 |
| <a name="provider_databricks.workspace"></a> [databricks.workspace](#provider\_databricks.workspace) | >= 1.48.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_permission_assignment.admin_user_assignments](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permission_assignment) | resource |
| [databricks_permission_assignment.group_assignments](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permission_assignment) | resource |
| [databricks_permission_assignment.user_assignments](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permission_assignment) | resource |
| [databricks_group.account_groups](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/group) | data source |
| [databricks_user.admin_users](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/user) | data source |
| [databricks_user.users](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/user) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_workspace_onboarding_config"></a> [workspace\_onboarding\_config](#input\_workspace\_onboarding\_config) | Full config for onboarding users and groups into workspace | <pre>object({<br/>    groups = optional(list(object({<br/>      name        = string<br/>      permissions = list(string)<br/>    })))<br/>    users       = optional(list(string))<br/>    admin_users = optional(list(string))<br/>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
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
| [databricks_grant.catalog_grants](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grant) | resource |
| [databricks_grant.schema_grants](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grant) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_unity_catalog_grants"></a> [unity\_catalog\_grants](#input\_unity\_catalog\_grants) | Permissions for catalogs and schemas in Unity Catalog | <pre>object({<br/>    catalogs = optional(list(object({<br/>      name   = string<br/>      grants = list(object({<br/>        principals   = list(string)<br/>        permissions = list(string)<br/>      }))<br/>    })))<br/><br/>    schemas = optional(list(object({<br/>      name   = string<br/>      grants = list(object({<br/>        principals   = list(string)<br/>        permissions = list(string)<br/>      }))<br/>    })))<br/>  })</pre> | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
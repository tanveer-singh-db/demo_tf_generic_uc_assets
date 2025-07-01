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
| <a name="module_uc_catalogs"></a> [uc\_catalogs](#module\_uc\_catalogs) | ../../databricks/uc_catalog | n/a |
| <a name="module_uc_external_locations"></a> [uc\_external\_locations](#module\_uc\_external\_locations) | ../../databricks/external_location | n/a |
| <a name="module_uc_schemas"></a> [uc\_schemas](#module\_uc\_schemas) | ../../databricks/uc_schema | n/a |
| <a name="module_uc_storage_creds"></a> [uc\_storage\_creds](#module\_uc\_storage\_creds) | ../../databricks/storage_credential | n/a |
| <a name="module_uc_tables"></a> [uc\_tables](#module\_uc\_tables) | ../../databricks/uc_table | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_uc_objects_config"></a> [uc\_objects\_config](#input\_uc\_objects\_config) | Databricks Unity Catalog deployment config | <pre>object({<br/>    # options = object({<br/>    #   create_storage_creds       = bool<br/>    #   create_external_locations  = bool<br/>    #   create_catalogs            = bool<br/>    #   create_schemas             = bool<br/>    # })<br/><br/>    storage_creds = optional(list(<br/>      object({<br/>        name             = string<br/>        comment          = optional(string)<br/>        metastore_id     = optional(string)<br/>        owner            = optional(string)<br/>        read_only        = optional(bool, false)<br/>        skip_validation  = optional(bool, false)<br/>        force_destroy    = optional(bool, false)<br/>        force_update     = optional(bool, false)<br/>        isolation_mode   = optional(string, "ISOLATION_MODE_ISOLATED")<br/>        access_connector_id = string<br/>      })<br/>    ))<br/><br/>    external_locations = optional(list(<br/>      object({<br/>        name               = string<br/>        url                = string       # Azure format: abfss://<container>@<storage_account>.dfs.core.windows.net/<path><br/>        credential_name    = string<br/>        owner              = optional(string)<br/>        comment            = optional(string)<br/>        skip_validation    = optional(bool, false)<br/>        fallback           = optional(bool, false)<br/>        read_only          = optional(bool, false)<br/>        force_destroy      = optional(bool, false)<br/>        force_update       = optional(bool, false)<br/>        isolation_mode     = optional(string, "ISOLATION_MODE_ISOLATED")<br/>      })<br/>    ))<br/><br/>    catalogs = optional(list(object({<br/>      name                         = string<br/>      storage_root                 = optional(string)<br/>      provider_name                = optional(string)<br/>      share_name                   = optional(string)<br/>      connection_name              = optional(string)<br/>      owner                        = optional(string)<br/>      isolation_mode               = optional(string, "ISOLATED")<br/>      enable_predictive_optimization = optional(string, "INHERIT")<br/>      comment                      = optional(string)<br/>      properties                   = optional(map(string))<br/>      options                      = optional(map(string))<br/>      force_destroy                = optional(bool, false)<br/>  })))<br/><br/>    schemas = optional(list(<br/>      object({<br/>        name                         = string<br/>        catalog_name                 = string<br/>        storage_root                 = optional(string)<br/>        owner                        = optional(string)<br/>        comment                      = optional(string)<br/>        properties                   = optional(map(string))<br/>        enable_predictive_optimization = optional(string, "INHERIT")<br/>        force_destroy                = optional(bool, false)<br/>      })<br/>    ))<br/><br/>    sql_tables = optional(list(<br/>      object({<br/>          name               = string<br/>          catalog_name       = string<br/>          schema_name        = string<br/>          table_type         = string<br/>          comment            = optional(string)<br/>          owner              = optional(string)<br/>          view_definition    = optional(string)<br/>          cluster_keys       = optional(list(string))<br/>          partitions         = optional(list(string))<br/>          data_source_format = optional(string)<br/>          storage_location   = optional(string)<br/>          options            = optional(map(string))<br/>          properties         = optional(map(string))<br/>          columns = optional(list(object({<br/>            name     = string<br/>            type     = optional(string, "string")<br/>            comment  = optional(string)<br/>            nullable = optional(bool, true)<br/>            identity = optional(string) # only "default" or "always"<br/>          })))<br/>      })<br/>    ))<br/><br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_catalog_names"></a> [catalog\_names](#output\_catalog\_names) | n/a |
| <a name="output_external_locations"></a> [external\_locations](#output\_external\_locations) | n/a |
| <a name="output_planned_external_locations"></a> [planned\_external\_locations](#output\_planned\_external\_locations) | n/a |
| <a name="output_schema_names"></a> [schema\_names](#output\_schema\_names) | n/a |
<!-- END_TF_DOCS -->
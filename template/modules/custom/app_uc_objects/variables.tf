
variable "uc_objects_config" {
  description = "Databricks Unity Catalog deployment config"
  type = object({
    # options = object({
    #   create_storage_creds       = bool
    #   create_external_locations  = bool
    #   create_catalogs            = bool
    #   create_schemas             = bool
    # })

    storage_creds = optional(list(
      object({
        name             = string
        comment          = optional(string)
        metastore_id     = optional(string)
        owner            = optional(string)
        read_only        = optional(bool, false)
        skip_validation  = optional(bool, false)
        force_destroy    = optional(bool, false)
        force_update     = optional(bool, false)
        isolation_mode   = optional(string, "ISOLATION_MODE_ISOLATED")
        access_connector_id = string
      })
    ))

    external_locations = optional(list(
      object({
        name               = string
        url                = string       # Azure format: abfss://<container>@<storage_account>.dfs.core.windows.net/<path>
        credential_name    = string
        owner              = optional(string)
        comment            = optional(string)
        skip_validation    = optional(bool, false)
        fallback           = optional(bool, false)
        read_only          = optional(bool, false)
        force_destroy      = optional(bool, false)
        force_update       = optional(bool, false)
        isolation_mode     = optional(string, "ISOLATION_MODE_ISOLATED")
      })
    ))

    catalogs = optional(list(object({
      name                         = string
      storage_root                 = optional(string)
      provider_name                = optional(string)
      share_name                   = optional(string)
      connection_name              = optional(string)
      owner                        = optional(string)
      isolation_mode               = optional(string, "ISOLATED")
      enable_predictive_optimization = optional(string, "INHERIT")
      comment                      = optional(string)
      properties                   = optional(map(string))
      options                      = optional(map(string))
      force_destroy                = optional(bool, false)
  })))

    schemas = optional(list(
      object({
        name                         = string
        catalog_name                 = string
        storage_root                 = optional(string)
        owner                        = optional(string)
        comment                      = optional(string)
        properties                   = optional(map(string))
        enable_predictive_optimization = optional(string, "INHERIT")
        force_destroy                = optional(bool, false)
      })
    ))

    sql_tables = optional(list(
      object({
          name               = string
          catalog_name       = string
          schema_name        = string
          table_type         = string
          comment            = optional(string)
          owner              = optional(string)
          view_definition    = optional(string)
          cluster_keys       = optional(list(string))
          partitions         = optional(list(string))
          data_source_format = optional(string)
          storage_location   = optional(string)
          options            = optional(map(string))
          properties         = optional(map(string))
          columns = optional(list(object({
            name     = string
            type     = optional(string, "string")
            comment  = optional(string)
            nullable = optional(bool, true)
            identity = optional(string) # only "default" or "always"
          })))
      })
    ))

  })
}

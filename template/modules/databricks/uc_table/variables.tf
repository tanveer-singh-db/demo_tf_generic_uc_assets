variable "sql_tables" {
  description = "List of SQL table definitions, each a map with keys like name, catalog_name, schema_name, etc."
  type = list(object({
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
  }))
  default = []
  validation {
    condition = var.sql_tables == null ? true :  alltrue([
      for t in var.sql_tables : contains(["MANAGED", "EXTERNAL", "VIEW"], t.table_type)
    ])
    error_message = "table_type must be 'MANAGED', 'EXTERNAL', or 'VIEW'."
  }

  validation {
    condition = var.sql_tables == null ? true :  alltrue([
      for t in var.sql_tables : (
      t.table_type != "EXTERNAL" || t.storage_location != null
      )
    ])
    error_message = "storage_location is required for EXTERNAL tables."
  }

  validation {
    condition = var.sql_tables == null ? true :  alltrue([
      for t in var.sql_tables : (
        t.cluster_keys == null || t.partitions == null
      )
    ])
    error_message = "Cannot set both cluster_keys and partitions for the same table."
  }

}


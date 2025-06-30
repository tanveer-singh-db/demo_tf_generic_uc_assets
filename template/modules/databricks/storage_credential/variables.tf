variable "storage_credential" {
  description = "Configuration for Azure storage credential"
  type = object({
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

  validation {
    condition = can(regex(
      "^/subscriptions/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/resourceGroups/[a-zA-Z0-9_-]+/providers/Microsoft\\.Databricks/accessConnectors/[a-zA-Z0-9_-]+$",
      var.storage_credential.access_connector_id
    ))
    error_message = "access_connector_id must be in the format: /subscriptions/<uuid>/resourceGroups/<resource-group>/providers/Microsoft.Databricks/accessConnectors/<connector-name>"
  }

  validation {
    condition = contains(
      ["ISOLATION_MODE_OPEN", "ISOLATION_MODE_ISOLATED"],
      coalesce(var.storage_credential.isolation_mode, "ISOLATION_MODE_OPEN")
    )
    error_message = "isolation_mode must be either 'ISOLATION_MODE_OPEN' or 'ISOLATION_MODE_ISOLATED'"
  }
}
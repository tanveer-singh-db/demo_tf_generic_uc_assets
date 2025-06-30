variable "external_location" {
  description = "Configuration for Azure external location"
  type = object({
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

  validation {
    condition = can(regex("^abfss://", var.external_location.url))
    error_message = "URL must be in Azure ABFSS format: abfss://<container>@<storage_account>.dfs.core.windows.net/<path>"
  }

  validation {
    condition = contains(
      ["ISOLATION_MODE_OPEN", "ISOLATION_MODE_ISOLATED"],
      coalesce(var.external_location.isolation_mode, "ISOLATION_MODE_OPEN")
    )
    error_message = "isolation_mode must be either 'ISOLATION_MODE_OPEN' or 'ISOLATION_MODE_ISOLATED'"
  }
}


variable "catalog" {
  description = "Configuration for a single catalog"
  type = object({
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
  })

  validation {
    condition = contains(["OPEN", "ISOLATED"], coalesce(var.catalog.isolation_mode, "OPEN"))
    error_message = "isolation_mode must be either 'OPEN' or 'ISOLATED'."
  }

  validation {
    condition = contains(["ENABLE", "DISABLE", "INHERIT"], coalesce(var.catalog.enable_predictive_optimization, "INHERIT"))
    error_message = "enable_predictive_optimization must be one of 'ENABLE', 'DISABLE', or 'INHERIT'."
  }
}
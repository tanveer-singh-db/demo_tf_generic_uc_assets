variable "schema" {
  description = "Configuration for a Databricks schema"
  type = object({
    name                         = string
    catalog_name                 = string
    storage_root                 = optional(string)
    owner                        = optional(string)
    comment                      = optional(string)
    properties                   = optional(map(string))
    enable_predictive_optimization = optional(string, "INHERIT")
    force_destroy                = optional(bool, false)
  })

  validation {
    condition = contains(
      ["ENABLE", "DISABLE", "INHERIT"],
      coalesce(var.schema.enable_predictive_optimization, "INHERIT")
    )
    error_message = "enable_predictive_optimization must be one of 'ENABLE', 'DISABLE', or 'INHERIT'."
  }
}
variable "delta_sharing_config" {
  type = object({
    recipients = optional(list(object({
      name                 = string
      recipient_sharing_id = string
      comment              = optional(string, "")
    })))
    shares = optional(list(object({
      name          = string
      recipient_names = optional(list(string), [])
      internal_recipient_catalog_name  = optional(string, null)
      objects       = list(object({
        type = string
        name = string
        history_data_sharing_status = optional(string, "ENABLED")
      }))
      comment = optional(string, "")
    })))
  })
  description = "Consolidated configuration for Delta Sharing setup"
}
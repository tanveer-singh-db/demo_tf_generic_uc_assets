variable "workspace_bindings" {
  description = "List of bindings, each workspace_URL, and catalogs"
  type = list(object({
    workspace_id = string
    # workspace_url = string
    catalogs      = optional(list(string),[])
    external_locations = optional(list(string),[])
    storage_credentials = optional(list(string),[])
    credentials = optional(list(string),[])
    binding_type = optional(string, "BINDING_TYPE_READ_ONLY")
  }))
  validation {
    condition = alltrue([
      for wb in var.workspace_bindings :
      contains(["BINDING_TYPE_READ_WRITE", "BINDING_TYPE_READ_ONLY"], coalesce(wb.binding_type, "BINDING_TYPE_READ_WRITE"))
    ])
    error_message = "binding_type must be either 'BINDING_TYPE_READ_ONLY' or 'BINDING_TYPE_READ_WRITE'."
  }


}
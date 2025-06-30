variable "workspace_onboarding_config" {
  description = "Full config for onboarding users and groups into workspace"
  type = object({
    groups = optional(list(object({
      name        = string
      permissions = list(string)
    })))
    users       = optional(list(string))
    admin_users = optional(list(string))
  })
}
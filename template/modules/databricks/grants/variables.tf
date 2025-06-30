variable "unity_catalog_grants" {
  description = "Permissions for catalogs and schemas in Unity Catalog"
  type = object({
    catalogs = optional(list(object({
      name   = string
      grants = list(object({
        principals   = list(string)
        permissions = list(string)
      }))
    })))

    schemas = optional(list(object({
      name   = string
      grants = list(object({
        principals   = list(string)
        permissions = list(string)
      }))
    })))
  })
}

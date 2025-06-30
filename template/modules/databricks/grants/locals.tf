# locals {
#
#   catalogs = try(var.unity_catalog_grants.catalogs, [])
#   schemas = try(var.unity_catalog_grants.schemas, [])
#
#   flattened_catalog_grants = flatten([
#     for catalog in local.catalogs : [
#       for grant in catalog.grants : {
#         catalog    = catalog.name
#         principal  = grant.principal
#         privileges = grant.permissions
#       }
#     ]
#   ])
#
#   flattened_schema_grants = flatten([
#     for schema in local.schemas : [
#       for grant in schema.grants : {
#         schema     = schema.name
#         principal  = grant.principal
#         privileges = grant.permissions
#       }
#     ]
#   ])
# }

locals {
  catalogs = try(var.unity_catalog_grants.catalogs, [])
  schemas  = try(var.unity_catalog_grants.schemas, [])

  flattened_catalog_grants = local.catalogs == null ? [] : flatten([
    for catalog in local.catalogs : [
      for grant in catalog.grants : [
        for principal in grant.principals : {
          catalog    = catalog.name
          principal  = principal
          privileges = grant.permissions
        }
      ]
    ]
  ])

  flattened_schema_grants = local.schemas == null ? [] : flatten([
    for schema in local.schemas : [
      for grant in schema.grants : [
        for principal in grant.principals : {
          schema     = schema.name
          principal  = principal
          privileges = grant.permissions
        }
      ]
    ]
  ])
}

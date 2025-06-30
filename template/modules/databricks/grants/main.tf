


resource "databricks_grant" "catalog_grants" {
  for_each = local.flattened_catalog_grants == null ? {} : {
    for grant in local.flattened_catalog_grants :
    "${grant.catalog}_${grant.principal}" => grant
  }

  catalog    = each.value.catalog
  principal  = each.value.principal
  privileges = each.value.privileges

  lifecycle {
    create_before_destroy = true
  }
}

resource "databricks_grant" "schema_grants" {
  for_each = local.flattened_schema_grants == null ? {} : {
    for grant in local.flattened_schema_grants :
    "${grant.schema}_${grant.principal}" => grant
  }

  schema     = each.value.schema
  principal  = each.value.principal
  privileges = each.value.privileges

  lifecycle {
    create_before_destroy = true
  }
}
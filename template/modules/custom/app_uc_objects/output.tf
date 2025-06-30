output "planned_external_locations" {
  value = local.external_locations
}


output "external_locations" {
  value = {
    for k, mod in module.uc_external_locations :
        k => mod.external_location_name
  }
}

output "catalog_names" {
  value = {
    for k, mod in module.uc_catalogs :
    k => mod.catalog_name
  }
}

output "schema_names" {
  value = {
    for k, mod in module.uc_schemas :
    k => mod.schema_name
  }
}
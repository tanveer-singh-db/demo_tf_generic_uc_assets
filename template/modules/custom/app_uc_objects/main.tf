
module "uc_storage_creds" {
  source = "../../databricks/storage_credential"
  for_each = local.storage_creds == null ? {} : { for cred in local.storage_creds: cred.name => cred}
  storage_credential = each.value
}

module "uc_external_locations"{
  source = "../../databricks/external_location"
  for_each = local.external_locations == null ? {} : { for ext_loc in local.external_locations: ext_loc.name => ext_loc}
  external_location = each.value
  depends_on = [module.uc_storage_creds]
}

# create catalogs
module "uc_catalogs" {
  source = "../../databricks/uc_catalog"
  for_each = local.catalogs == null ? {} : { for catalog in local.catalogs: catalog.name => catalog}
  catalog = each.value
  depends_on = [module.uc_external_locations]

}
module "uc_schemas" {
  source = "../../databricks/uc_schema"
  for_each = local.schemas == null ? {}: { for schema in local.schemas: schema.name => schema}
  schema = each.value
  depends_on = [module.uc_catalogs ]
}

module "uc_tables" {
  source= "../../databricks/uc_table"
  sql_tables = local.tables
  depends_on = [module.uc_schemas]
}
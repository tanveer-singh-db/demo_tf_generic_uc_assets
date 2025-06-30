locals {

  catalogs = try(var.uc_objects_config.catalogs,[])

  schemas = try(var.uc_objects_config.schemas,[])

  storage_creds = try(var.uc_objects_config.storage_creds,[])

  external_locations = try(var.uc_objects_config.external_locations, [])

  tables = try(var.uc_objects_config.sql_tables, [])

}
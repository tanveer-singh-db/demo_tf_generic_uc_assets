output "debug_config_base_path" {
  value = local.config_base_path
}


output "debug_merged_config" {
  value = local.merged_config
}

# output "debug_metastore_info" {
#   value = module.delta_sharing.current_metastore_id
# }


output "debug_uc_object_config" {
  value = local.uc_object_config
}

output "planned_external_locations" {
  value = module.app_uc_objects.planned_external_locations
}

output "external_locations" {
  value = module.app_uc_objects.external_locations
}
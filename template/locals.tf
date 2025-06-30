locals {
  # Full path to config YAML: {root_dir}/configs/<env>/<bu>/config.yml
  config_base_path = "../${var.cloudEnvironment}/${var.region}/${var.workspaceInfo}"

  # uc_object_config = try(yamldecode(file("${local.config_base_path}/${var.uc_objects_config_file}")),{})
  #
  # uc_object_grants_config = try(yamldecode(file("${local.config_base_path}/${var.uc_object_grants_config_file}")),{})
  #
  # workspace_binding_config = try(yamldecode(file("${local.config_base_path}/${var.workspace_binding_config_file}")),{})
  #
  # delta_sharing_config =  try(yamldecode(file("${local.config_base_path}/${var.delta_sharing_config_file}")),{})

  # Get all YAML files in the config directory
  yaml_files = fileset(local.config_base_path, "*.{yaml,yml}")

  # Parse all YAML files into a map with full filename as the key
  yaml_configs = {
    for file in local.yaml_files :
    file => try(yamldecode(file("${local.config_base_path}/${file}")), {})
  }

  # Merge all YAML configs into a single map
  merged_config = merge([
    for file, config in local.yaml_configs : config
  ]...)

  uc_object_config = {
    external_locations = try(local.merged_config.external_locations, [])
    catalogs = try(local.merged_config.catalogs, [])
    schemas = try(local.merged_config.schemas, [])
    sql_tables = try(local.merged_config.sql_tables, [])
  }

delta_sharing_config = {
    recipients = try(lookup(local.merged_config, "recipients", []), [])
    shares     = try(lookup(local.merged_config, "shares", []), [])
  }

  uc_object_grants_config = try(local.merged_config.uc_object_grants, {})

  workspace_bindings_config = try(local.merged_config.workspace_bindings, [])

}
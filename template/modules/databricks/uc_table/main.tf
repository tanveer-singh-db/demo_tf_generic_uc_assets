
resource "databricks_sql_table" "this" {
  for_each = var.sql_tables == null ? {} : { for table in var.sql_tables : table.name => table }

  name               = each.value.name
  catalog_name       = each.value.catalog_name
  schema_name        = each.value.schema_name
  table_type         = each.value.table_type
  comment            = lookup(each.value, "comment", null)
  owner              = lookup(each.value, "owner", null)
  view_definition    = each.value.table_type == "VIEW" ? lookup(each.value, "view_definition", null) : null
  cluster_keys       = contains(["MANAGED", "EXTERNAL"], each.value.table_type) ? lookup(each.value, "cluster_keys", null) : null
  partitions         = contains(["MANAGED", "EXTERNAL"], each.value.table_type) ? lookup(each.value, "partitions", null) : null
  data_source_format = contains(["MANAGED", "EXTERNAL"], each.value.table_type) ? lookup(each.value, "data_source_format", null) : null
  options            = lookup(each.value, "options", null)
  properties         = lookup(each.value, "properties", null)
  storage_location   = each.value.table_type == "EXTERNAL" ? lookup(each.value, "storage_location", null) : null

  dynamic "column" {
    for_each = each.value.table_type != "VIEW" ? each.value.columns != null ? each.value.columns: [] : []
    content {
      name     = column.value.name
      type     = lookup(column.value, "type", "string")
      comment  = lookup(column.value, "comment", null)
      nullable = lookup(column.value, "nullable", true)
      identity = contains(keys(column.value), "identity") ? column.value.identity : null
    }
  }

}


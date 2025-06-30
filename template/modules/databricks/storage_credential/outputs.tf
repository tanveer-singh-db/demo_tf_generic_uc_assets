

# output "security_warning" {
#   value = (
#     var.storage_credential.isolation_mode == "ISOLATION_MODE_OPEN"
#     ? "WARNING: Using ISOLATION_MODE_OPEN reduces security. Only use if absolutely necessary."
#     : null
#   )
# }

output "storage_credential_id" {
  value = databricks_storage_credential.this.id
}

output "storage_credential_name" {
  value = databricks_storage_credential.this.name
}

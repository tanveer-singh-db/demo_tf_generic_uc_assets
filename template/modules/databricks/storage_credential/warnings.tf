# Custom check for isolation mode security warning
# check "isolation_mode_security" {
#   # This will always run during plan
#   data "terraform_data" "dummy" {
#     input = var.storage_credential.isolation_mode
#   }
#
#   # Condition that "fails" when we want to show a warning
#   assert {
#     condition = var.storage_credential.isolation_mode != "ISOLATION_MODE_OPEN"
#     error_message = <<-EOT
#     WARNING: Using ISOLATION_MODE_OPEN reduces security by making this storage credential
#     accessible from all workspaces. This is not recommended for production environments.
#
#     Only use ISOLATION_MODE_OPEN if you have a specific requirement for cross-workspace access.
#     EOT
#   }
# }
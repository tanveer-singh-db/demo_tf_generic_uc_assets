

resource "databricks_external_location" "this" {
  name            = var.external_location.name
  url             = var.external_location.url
  credential_name = var.external_location.credential_name
  owner           = var.external_location.owner
  comment         = var.external_location.comment
  skip_validation = var.external_location.skip_validation
  fallback        = var.external_location.fallback
  read_only       = var.external_location.read_only
  force_destroy   = var.external_location.force_destroy
  force_update    = var.external_location.force_update
  isolation_mode  = var.external_location.isolation_mode
}
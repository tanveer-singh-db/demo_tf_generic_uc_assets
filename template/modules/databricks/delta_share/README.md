<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_databricks"></a> [databricks](#requirement\_databricks) | >= 1.48.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_databricks"></a> [databricks](#provider\_databricks) | >= 1.48.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_grant.share_grant](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grant) | resource |
| [databricks_recipient.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/recipient) | resource |
| [databricks_share.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/share) | resource |
| [databricks_current_metastore.current](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/current_metastore) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_delta_sharing_config"></a> [delta\_sharing\_config](#input\_delta\_sharing\_config) | Consolidated configuration for Delta Sharing setup | <pre>object({<br/>    recipients = optional(list(object({<br/>      name                 = string<br/>      recipient_sharing_id = string<br/>      comment              = optional(string, "")<br/>    })))<br/>    shares = optional(list(object({<br/>      name          = string<br/>      recipient_names = optional(list(string), [])<br/>      internal_recipient_catalog_name  = optional(string, null)<br/>      objects       = list(object({<br/>        type = string<br/>        name = string<br/>        history_data_sharing_status = optional(string, "ENABLED")<br/>      }))<br/>      comment = optional(string, "")<br/>    })))<br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_recipient_ids"></a> [recipient\_ids](#output\_recipient\_ids) | n/a |
| <a name="output_share_ids"></a> [share\_ids](#output\_share\_ids) | n/a |
<!-- END_TF_DOCS -->
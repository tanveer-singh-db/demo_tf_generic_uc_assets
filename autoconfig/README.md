## Customized Terraform YAML Configuration Generation Tool

The `run_autoconfig.py` script automates the generation of customized Unity Catalog configuration files from meta templates, enabling users to control Terraform resource deployment through simple config modifications without changing Terraform code directly.

### Features
- **Template-based Config Generation**: Uses meta configuration templates to generate standardized UC objects YAML config for downstream Terraform deployment.
- **Dynamic User Schema Generation**: Automatically creates personal schemas for users from specified Databricks groups

### Arguments

#### Required Arguments
- `--bu` - Business unit name
- `--sub_domain` - Subdomain name
- `--workspace_info` - Unique workspace ID (e.g., "6208")

#### Optional Arguments
- `--app_name` - Application name
- `--meta_config_root` - Path to meta_configs directory (default: "./meta_configs")
- `--meta_file_name` - Meta template file name (default: "meta_bu_subdomain_app_template.yml")
- `--cloud_environment` - Environment name (default: "dev")
- `--region` - Azure region (default: "westeurope")
- `--subscription_id` - Azure subscription ID
- `--databricks_workspace_url` - Databricks workspace URL (required for user schema generation)
- `--databricks_token` - Databricks API token (required for user schema generation)
- `--output_root` - Output directory for generated files (default: current directory)

#### User Schema Generation Arguments
- `--generate_user_schemas` - Enable dynamic user schema generation from Databricks groups
- `--user_groups` - Space-separated list of Databricks group names (e.g., "data-scientists data-engineers")
- `--user_schema_template` - Template for user schema names (default: "<user_name>_schema")

### Usage Examples

#### Basic Configuration Generation
```bash
python run_autoconfig.py \
  --bu finance \
  --sub_domain reporting \
  --workspace_info 6208
```

#### Usage with User Schema Generation
```bash
python run_autoconfig.py \
  --bu finance \
  --sub_domain reporting \
  --workspace_info 6208 \
  --databricks_workspace_url "https://adb-1234567890123456.78.azuredatabricks.net" \
  --databricks_token $DATABRICKS_WS_TOKEN \
  --generate_user_schemas \
  --user_groups "data-scientists" "data-engineers" "analysts" \
  --app_name loan \
  --user_schema_template "<prefix>_<user_name>_schema"
```

#### Assign a Custom Template and Output Location
```bash
python run_autoconfig.py \
  --bu marketing \
  --sub_domain campaigns \
  --workspace_info 6209 \
  --meta_file_name "custom_template.yml" \
  --output_root "/custom/output/path" \
  --cloud_environment prod \
  --region southeastasia
```

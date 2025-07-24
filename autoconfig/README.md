# Unity Catalog Configuration Validator

This tool validates Unity Catalog configuration files against Azure resources and Databricks Unity Catalog requirements.

## Features
- Validates configuration file structure
- Checks metastore assignment in Databricks workspace
- Verifies existence of Azure storage accounts and containers
- Validates storage credentials in Unity Catalog
- Ensures container uniqueness across UC objects
- Comprehensive error reporting

## Prerequisites
1. Python 3.7+
2. Azure service principal with:
   - `Reader` access to Azure subscriptions
   - Storage account access
3. Databricks workspace with:
   - Unity Catalog enabled
   - Workspace admin privileges
4. Azure CLI Authentication for both Azure and Databricks Workspaces


## CLI Usage

The package provides a command-line interface for configuration validation:

```bash
python run_config_validator.py \
    --config_dir ./configs \
    --workspace_url https://your-workspace.cloud.databricks.com \
    --subscription_id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--config_dir` | Path to directory containing YAML configs | Yes |
| `--workspace_url` | Databricks workspace URL | Yes |
| `--subscription_id` | Azure subscription ID | Yes |


## Python API Usage

You can also use the validator programmatically:

```python
from autoconfig.config_validator import ConfigValidator

validator = ConfigValidator(
    config_dir="./configs",
    workspace_url="https://your-workspace.cloud.databricks.com",
    subscription_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
)

errors = validator.validate()
if errors:
    print("Validation failed:")
    for error in errors:
        print(f"- {error}")
else:
    print("Validation successful!")
```



## Development

### Dependencies

- Python 3.7+
- Pydantic
- Azure SDK
- Databricks SDK

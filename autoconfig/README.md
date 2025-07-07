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
4. Environment variables configured:
   ```bash
   export AZURE_SUBSCRIPTION_ID="<your-azure-subscription-id>"
   export DATABRICKS_HOST="<your-databricks-workspace-url>"
   export DATABRICKS_TOKEN="<your-databricks-access-token>"
   ```

## Installation
```shell
# Clone repository
git clone https://github.com/your-repo/unity-catalog-validator.git
cd unity-catalog-validator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
## Usage
```shell
python -m autoconfig.cli path/to/config.yaml
```

### Exit Codes
| Code | Meaning                         |
|------|---------------------------------|
| 0    | Validation successful           |
| 1    | Validation errors detected      |
| 2    | Config file loading error       |
| 3    | Missing environment variables   |
| 4    | Unexpected runtime error        |



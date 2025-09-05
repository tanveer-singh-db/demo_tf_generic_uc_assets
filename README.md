# Databricks Unity Catalog Terraform Deployment

This repository provides a solution for deploying Databricks Unity Catalog (UC) resources using Terraform, with automated config generation and pre-deployment validation tools.

## Table of Contents
- [Overview](#overview)
- [Key Concepts](#key-concepts)
- [Quick Start](#quick-start)
- [What You Get](#what-you-get)
- [Directory Structure](#directory-structure)
- [Three Main Tools](#three-main-tools)
- [Prerequisites](#prerequisites)
- [Detailed Usage](#detailed-usage)
- [Configuration Structure](#configuration-structure)
- [FAQ](#faq)
- [Command Reference](#command-reference)

## Overview

Unity Catalog is Databricks’ unified governance solution for all data and AI assets. This module automates:
- Creation of catalogs, schemas, tables, external locations
- Managing storage credentials, workspace bindings, and grants
- Delta sharing configurations and recipient management

The project using a config-driven approach.

---

## Key Concepts
- Config-driven: Deployment controlled by *.tfvars or YAML-converted inputs

- Resuable: Modules can be reused

---

## Quick Start

### 1. Generate Configuration (First Time Setup)
```bash
# Generate UC configuration from templates
python run_autoconfig.py \
  --bu finance \
  --sub_domain reporting \
  --workspace_info 6208

# With dynamic user schemas from Databricks groups
python run_autoconfig.py \
  --bu finance \
  --sub_domain reporting \
  --workspace_info 6208 \
  --databricks_workspace_url "https://adb-1234567890123456.78.azuredatabricks.net" \
  --databricks_token $DATABRICKS_WS_TOKEN \
  --generate_user_schemas \
  --user_groups "data-scientists" "data-engineers"
```

### 2. Validate Configuration - UC Check
```bash
# Validate against Azure and Databricks before deployment
python run_config_validator.py \
  --config_dir ../dev/southeastasia/2178 \
  --workspace_url https://your-workspace.cloud.databricks.com \
  --subscription_id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 3. Deploy with Terraform
```bash
cd template/
terraform init -reconfigure -backend-config=../dev/southeastasia/2178/config.tfbackend
terraform plan -var-file=../dev/southeastasia/2178/terraform.tfvars
terraform apply -var-file=../dev/southeastasia/2178/terraform.tfvars
```

## What You Get

- **Unity Catalog Objects**: Catalogs, schemas, tables, external locations
- **Access Control**: Grants and permissions across all resources
- **Delta Sharing**: Recipients, shares, and sharing permissions
- **Workspace Bindings**: Link catalogs to specific workspaces
- **Configuration Validation**: Pre-deployment UC checks for Azure resources and UC requirements

## Directory Structure

```
📂 project-root/
├── 📁 template/           # Main Terraform deployment
├── 📁 autoconfig/         # Configuration generation tool
├── 📁 uc_check/          # Pre-deployment validation
├── 📁 meta_configs/      # Template configurations
├── 📁 sample_config_templates/  # Example config files
└── 📁 dev/qa/prod/       # Environment-specific configs
    └── 📁 {region}/      # Region-specific configs
        └── 📁 {workspace}/  # Workspace-specific configs
```

## 3 Main Tools

### 1. TF UC YAML Configuration Generator (`autoconfig/`)
**Purpose**: Generate standardized UC configurations from templates

Automates the creation of customized Unity Catalog configuration files from meta templates, enabling users to control Terraform resource deployment through config modifications.

**See [autoconfig/README.md](autoconfig/README.md) for detailed usage instructions and examples**

### 2. Configuration Validator (`uc_check/`)
**Purpose**: Validate TF UC YAML configurations before deployment

**Key features**:
- Pre-deployment validation

**See [uc_check/README.md](uc_check/README.md) for detailed validation features and usage**


### 3. Terraform Deployment (`template/`)
**Purpose**: Deploy Unity Catalog resources to Databricks workspaces

**What it does**:
- Creates catalogs, schemas, tables, and external locations
- Applies grants and access policies
- Sets up Delta Sharing recipients and shares
- Binds catalogs to specific workspaces


## Prerequisites

### Azure Resources
- **Storage Accounts and Containers**: Must be created before UC object deployment
- **Storage Credentials**: Must exist in Databricks before deployment
- **Metastore Assignment**: Workspace must have metastore assigned

### Service Principal Permissions
The service principal must have these **metastore-level** permissions:
- `CREATE_CATALOG`, `CREATE_SCHEMA`, `CREATE_EXTERNAL_LOCATION`
- `CREATE_PROVIDER`, `CREATE_RECIPIENT`, `CREATE_SHARE`
- `USE_PROVIDER`, `USE_RECIPIENT`, `USE_SHARE`, `SET_SHARE_PERMISSION`
- Optional: `CREATE_CONNECTION`, `CREATE_CLEAN_ROOM`, `USE_MARKETPLACE_ASSETS`

### Required Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `databricks_workspace_url` | Databricks workspace URL | `https://adb-123.azuredatabricks.net` |
| `deployment_tenant_id` | Azure tenant ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `cloudEnvironment` | Environment directory | `dev`, `qa`, `prod` |
| `region` | Region directory | `southeastasia`, `westeurope` |
| `workspaceInfo` | Workspace directory | `2178`, `6208` |

## Detailed Usage

### Use Autoconfig Tool (Recommended for New Setups)
```bash
# Generate configuration from templates - see autoconfig/README.md for all options
cd autoconfig/
python run_autoconfig.py --bu finance --sub_domain reporting --workspace_info 6208

# Then deploy
cd ../template/
terraform init -reconfigure -backend-config=../dev/southeastasia/6208/config.tfbackend
terraform apply -var-file=../dev/southeastasia/6208/terraform.tfvars
```


## Configuration Structure

Your configuration directory should contain:
- `uc_objects.yml` - Defines catalogs, schemas, tables, external locations
- `uc_object_grants.yml` - Permission configurations
- `workspace_binding.yml` - Workspace-to-catalog bindings
- `delta_shares.yml` - Delta sharing recipients and shares
- `terraform.tfvars` - Terraform variable definitions
- `config.tfbackend` - Backend configuration for state management

## FAQ
**Q: How do I add user schemas dynamically?**
A: Use the autoconfig tool with `--generate_user_schemas` and specify Databricks groups with `--user_groups`.

**Q: What happens if I run deployment on an existing setup?**
A: Terraform will show a plan of changes. Existing resources won't be destroyed unless explicitly removed from config.

**Q: Can I customize the naming conventions?**
A: Yes, modify the meta templates in `meta_configs/` or use the template variables in autoconfig.

**Q: How do I validate my configuration before deployment?**
A: Use the UC validator: `cd uc_check/ && python run_config_validator.py --config_dir ../path/to/config`

## Command Reference

### Configuration Generation
```bash
cd autoconfig/
python run_autoconfig.py --bu <business_unit> --sub_domain <subdomain> --workspace_info <workspace_id>
# See autoconfig/README.md for all parameters and advanced options
```

### Configuration Validation
```bash
cd uc_check/
python run_config_validator.py --config_dir <path> --workspace_url <url> --subscription_id <id>
# See uc_check/README.md for detailed validation features
```

### Terraform Deployment
```bash
cd template/
terraform init -reconfigure -backend-config=../<env>/<region>/<workspace>/config.tfbackend
terraform plan -var-file=../<env>/<region>/<workspace>/terraform.tfvars
terraform apply -var-file=../<env>/<region>/<workspace>/terraform.tfvars
```

### Terraform Utilities
```bash
terraform fmt        # Format all files
terraform validate             # Validate configuration
terraform destroy             # Remove all resources
```

---

## Additional Documentation
- **[Autoconfig Tool Details](autoconfig/README.md)**
- **[UC Validator Details](uc_check/README.md)**
- **[Terraform Module Details](template/README.md)**

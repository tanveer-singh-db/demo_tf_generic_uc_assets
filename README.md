# Terraform UC Deployment

This repository provides a configurable and modular Terraform setup to deploy [Databricks Unity Catalog (UC)] resources across workspaces and metastores in a standardized, reusable, and scalable manner.

## 🔍 Overview

Unity Catalog is Databricks’ unified governance solution for all data and AI assets. This module automates:
- Creation of catalogs, schemas, tables, external locations
- Managing storage credentials, workspace bindings, and grants
- Delta sharing configurations and recipient management

The project supports multi-cloud and multi-metastore deployments using a config-driven approach with minimal hardcoding.

---

## Key Concepts
- Config-driven: Deployment controlled by *.tfvars or YAML-converted inputs

- Metastore-aware: Resources are filtered and applied only if workspace-metastore match

- Composable: Modules can be reused or omitted selectively

- Scalable: Designed for multi-workspace, multi-region setups


---

## 🚀 Use Cases

- Automate provisioning of Unity Catalog resources across multiple Databricks workspaces
- Apply consistent grants and access policies across catalogs and schemas
- Integrate Delta Sharing with internal and external recipients
- Bootstrap new data products and environments with minimal manual setup

## Modules

The system is composed of loosely coupled modules orchestrated through configuration and Terraform `for_each` constructs. 
A single execution plan can:
- Create external_location, catalogs, schemas and tables
- Set grants at both schema and catalog level
- Configure Delta Sharing shares and recipients
- Apply workspace bindings (only if workspace/metastore IDs match)


---
## Pre-Requisites

- **Storage Accounts** and **Containers** must be created prior to creating catalogs and schemas
- **Storage Credentials** must be pre-created prior to creation of the Unity Catalog Objects
- The **Service Account** or **Service Principal** being used for this terraform deployment, 
  must have the following permissions at the **Metastore** level:

    * CREATE_CATALOG
    * CREATE_SCHEMA
    * CREATE_EXTERNAL_LOCATION
    * CREATE_PROVIDER
    * CREATE_RECIPIENT
    * CREATE_SHARE
    * USE_PROVIDER
    * USE_RECIPIENT
    * USE_SHARE
    * SET_SHARE_PERMISSION
    * (Optional) CREATE_CONNECTION, CREATE_CLEAN_ROOM, USE_MARKETPLACE_ASSETS



## Planned checks for pre-requisites
1. Check if metastore is assigned to the workspace.
2. Check if storage_accounts and containers are created prior to deployment.
3. Check if the storage_credential provided has been created prior to deployment.
3. Check if the container@storage_account being used for a UC Object (Catalog, Schema) has already been used for a different UC Object.
4. Check if provided config structure matches the expected structure by the module.

## Parameters Required

- databricks_workspace_url : https://<workspace>.azuredatabricks.net
- deployment_tenant_id : Azure tenant ID where the databricks workspace has been deployed
- cloudEnvironment: The cloud environment dir where the config yaml files exist, i.e. dev, qa, prod
- region: The region dir where the config yaml files exist, i.e. southeastasia, westeurope
- workspaceInfo: Refers to the workspace info dir, where the config yaml files exist

## Usage

```shell
terraform init -reconfigure -backend-config=../<cloudEnvironment>/<region>/<workspaceInfo>/config.tfbackend
```
```shell
terraform plan -var-file=../<cloudEnvironment>/<region>/<workspaceInfo>/terraform.tfvars
```


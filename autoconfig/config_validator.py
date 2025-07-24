"""
Unity Catalog Configuration Validator

This module provides functionality to validate Unity Catalog configurations
against Azure resources and Databricks workspace settings.
"""
import pathlib
import re
from collections import ChainMap
from typing import Dict, List, Tuple, Optional

import yaml
from pydantic import BaseModel, ValidationError
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccount
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import StorageCredentialInfo

from autoconfig.common.logging_utils import get_log
from autoconfig.common.utils import get_exception
from autoconfig.validation_models import UcObjectsConfig, DeltaSharingConfig


class ConfigValidator:
    """
        Validates Unity Catalog configuration against Azure resources and Databricks workspace.

        This class performs comprehensive validation including:
        - Configuration file structure validation
        - Azure storage resource existence checks
        - Databricks Unity Catalog object validation
        - Container uniqueness verification
        """
    def __init__(self, config_dir: str,
                 subscription_id: str,
                 workspace_url: str):
        """
        Initialize the validator with configuration and connection details.

        Args:
            config_dir: Path to directory containing YAML configuration files
            subscription_id: Azure subscription ID for storage validation
            workspace_url: Databricks workspace URL for API connections
        """
        self.log = get_log("config_validator")
        self.config_dir = config_dir

        self.subscription_id = subscription_id
        self.workspace_url = workspace_url
        # self.azure_credential = DefaultAzureCredential()
        self.azure_credential =  DefaultAzureCredential(
            exclude_interactive_browser_credential=False,
            exclude_managed_identity_credential=False
        )
        self.storage_client = StorageManagementClient(self.azure_credential, subscription_id)
        self.errors: List[str] = []
        self.container_usage: Dict[Tuple[str, str], List[str]] = {}
        self.merged_config = None
        self.db_client = None
        self._set_config()
        self._set_workspace_client()

    def _set_workspace_client(self):
        """Initialize Databricks WorkspaceClient with Azure CLI authentication."""
        self.db_client = WorkspaceClient(
            host=self.workspace_url,
            auth_type="azure-cli",
        )

    def _set_config(self):
        """
        Load and merge all YAML configuration files from the config directory.

        Raises:
            FileNotFoundError: If config directory doesn't exist
            RuntimeError: If any YAML file fails to load
        """
        config_path = pathlib.Path(self.config_dir)
        # Validate config directory exists
        if not config_path.is_dir():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

        # Find all YAML files (both .yaml and .yml)
        yaml_files = sorted(config_path.glob("*.yaml")) + sorted(config_path.glob("*.yml"))

        # Parse all YAML files into a dictionary
        configs = {}
        for file_path in yaml_files:
            try:
                with open(file_path, 'r') as f:
                    # Use safe_load to prevent arbitrary code execution
                    configs[str(file_path)] = yaml.safe_load(f) or {}
            except (yaml.YAMLError, OSError) as e:
                raise RuntimeError(f"Error loading config file {file_path}: {str(e)}")

        # Merge all configurations using a chainmap (later files override earlier ones)
        self.merged_config = dict(ChainMap(*reversed(list(configs.values()))))



    def _validate_config_structure(self) -> bool:
        """
        Validate configuration structure using Pydantic models.

        Returns:
            bool: True if validation succeeds, False otherwise
        """
        try:
            # Define nested Pydantic models for structure validation
            # Define Pydantic models for UC Objects


            # Root configuration model
            class RootConfig(BaseModel):
                """Root configuration model combining all validation models."""
                uc_objects_config: Optional[UcObjectsConfig] = None
                delta_sharing_config: Optional[DeltaSharingConfig] = None

            RootConfig(**self.merged_config)
            return True
        except ValidationError as e:
            self.errors.append(f"Config structure validation failed: {str(e)}")
            return False

    def _check_metastore_assignment(self):
        """Verify metastore is assigned to workspace"""
        try:
            if not self.db_client.metastores.current():
                self.errors.append("No metastore assigned to this workspace")
        except Exception as e:
            self.errors.append(f"Metastore check failed: {str(e)}")

    def _check_storage_resources(self):
        """Validate storage accounts and containers exist in Azure"""
        storage_accounts = set()
        containers = set()

        # Collect all storage references from configuration
        for section in ['external_locations', 'catalogs', 'schemas']:
            for item in self.merged_config.get(section, []):
                url = item.get('url') or item.get('storage_root', '')
                if not url:
                    continue

                account, container = self._parse_abfss_url(url)
                if account and container:
                    storage_accounts.add(account)
                    containers.add((account, container))

        # Check storage accounts
        for account in storage_accounts:
            if not self._storage_account_exists(account):
                self.errors.append(f"Storage account does not exist: {account}")

        # Check containers
        for account, container in containers:
            if not self._container_exists(account, container):
                self.errors.append(f"Container does not exist: {container}@{account}")

    def _check_storage_credentials(self):
        """Verify all referenced storage credentials exist in Unity Catalog."""
        try:
            existing_creds = [c.name for c in self.db_client.storage_credentials.list()]

            for loc in self.merged_config.get('external_locations', []):
                cred_name = loc.get('credential_name')
                if cred_name and cred_name not in existing_creds:
                    self.errors.append(f"Storage credential not found: {cred_name}")
        except Exception as e:
            self.errors.append(f"Credential check failed: {str(e)}")

    def _check_container_uniqueness(self):
        """Ensure containers aren't reused across different UC objects."""
        for section in ['catalogs', 'schemas']:
            for item in self.merged_config.get(section, []):
                url = item.get('storage_root', '')
                if not url:
                    continue

                account, container = self._parse_abfss_url(url)
                if not account or not container:
                    continue

                key = (account, container)
                obj_ref = f"{section[:-1]}={item['name']}"

                if key in self.container_usage:
                    self.container_usage[key].append(obj_ref)
                else:
                    self.container_usage[key] = [obj_ref]

        # Find reused containers
        for (account, container), used_by in self.container_usage.items():
            if len(used_by) > 1:
                self.errors.append(
                    f"Container {container}@{account} reused by: {', '.join(used_by)}"
                )

    def _parse_abfss_url(self, url: str) -> Tuple[str, str]:
        """
        Parse ABFSS URL to extract storage account and container names.

        Args:
            url: ABFSS URL to parse (format: abfss://container@account.dfs.core.windows.net)

        Returns:
            Tuple of (account_name, container_name) or ("", "") if parsing fails
        """
        pattern = r"abfss://([^@]+)@([^.]+)\.dfs\.core\.windows\.net"
        match = re.match(pattern, url)
        if match:
            return match.group(2), match.group(1)
        return "", ""

    def _storage_account_exists(self, account_name: str) -> bool:
        """
        Check if storage account exists in Azure subscription.

        Args:
            account_name: Name of the storage account to check

        Returns:
            bool: True if account exists, False otherwise
        """
        try:
            for account in self.storage_client.storage_accounts.list():
                if account.name == account_name:
                    return True
        except:
            e = get_exception()
            self.log.warning(e)
            return False

    def _container_exists(self, account_name: str, container_name: str) -> bool:
        """
        Check if blob container exists in specified storage account.

        Args:
            account_name: Storage account name
            container_name: Container name to check

        Returns:
            bool: True if container exists, False otherwise
        """
        try:
            # Find the storage account and extract its resource group
            for account in self.storage_client.storage_accounts.list():
                if account.name == account_name:
                    account_id = account.id
                    rg = account_id.split('/')[4]  # /subscriptions/<sub_id>/resourceGroups/<rg>/...

                    # Check if the container exists
                    container = self.storage_client.blob_containers.get(
                        resource_group_name=rg,
                        account_name=account_name,
                        container_name=container_name
                    )
                    return bool(container)
            return False # if storage account not found
        except:
            e = get_exception()
            self.log.warning(e)
            return False

    def validate(self) -> List[str]:
        """
        Execute all validation checks in sequence.

        Returns:
            List of error messages (empty list indicates successful validation)
        """
        self.errors = []

        if not self._validate_config_structure():
            return self.errors  # Stop if structure is invalid
        self.log.info(f"Config structure validated successfully")
        self._check_metastore_assignment()
        self._check_storage_resources()
        self._check_storage_credentials()
        self._check_container_uniqueness()

        return self.errors

"""
Pydantic models for Unity Catalog configuration validation.

This module defines data models used to validate Unity Catalog configurations
for Databricks deployments including grants, objects, and delta sharing configs.
"""
from typing import List, Optional, Dict

from pydantic import BaseModel, ValidationError


# Define Pydantic models for Grants Configuration
class Grant(BaseModel):
    """
    Unity Catalog grant configuration.

    Attributes:
        principals: List of principals (users/groups/service principals) to grant permissions to
        permissions: List of permissions to grant
    """
    principals: List[str]
    permissions: List[str]

class CatalogGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog catalog.

    Attributes:
        name: Name of the catalog
        grants: List of grant configurations to apply to this catalog
    """
    name: str
    grants: List[Grant]

class SchemaGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog schema.

    Attributes:
        name: Fully schema name (catalog.schema)
        grants: List of grant configurations to apply to this schema
    """
    name: str
    grants: List[Grant]

class ExternalLocationGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog external location.

    Attributes:
        name: Name of the external location
        grants: List of grant configurations to apply to this external location
    """
    name: str
    grants: List[Grant]

class VolumeGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog volume.

    Attributes:
        name: Fully volume name (catalog.schema.volume)
        grants: List of grant configurations to apply to this volume
    """
    name: str  # Fully 3-level name: catalog.schema.volume
    grants: List[Grant]

class TableGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog table.

    Attributes:
        name: Fully table name (catalog.schema.table)
        grants: List of grant configurations to apply to this table
    """
    name: str  # Fully 3-level name: catalog.schema.table
    grants: List[Grant]

class FunctionGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog function.

    Attributes:
        name: Fully function name (catalog.schema.function)
        grants: List of grant configurations to apply to this function
    """
    name: str  # Fully 3-level name: catalog.schema.function
    grants: List[Grant]

class ModelGrant(BaseModel):
    """
    Grant configuration for a Unity Catalog ML model.

    Attributes:
        name: Fully 3-level model name (catalog.schema.model)
        grants: List of grant configurations to apply to this model
    """
    name: str  # Fully 3-level name: catalog.schema.model
    grants: List[Grant]

class UcObjectGrantsConfig(BaseModel):
    """
    Unity Catalog object grants configuration.

    Attributes:
        catalogs: Grant configurations for catalogs
        schemas: Grant configurations for schemas
        external_locations: Grant configurations for external locations
        volumes: Grant configurations for volumes
        tables: Grant configurations for tables
        functions: Grant configurations for functions
        models: Grant configurations for ML models
    """
    catalogs: Optional[List[CatalogGrant]] = None
    schemas: Optional[List[SchemaGrant]] = None
    external_locations: Optional[List[ExternalLocationGrant]] = None
    volumes: Optional[List[VolumeGrant]] = None
    tables: Optional[List[TableGrant]] = None
    functions: Optional[List[FunctionGrant]] = None
    models: Optional[List[ModelGrant]] = None


class StorageCredInfo(BaseModel):
    """
    Storage credential configuration.

    Attributes:
        name: Name of the storage credential
        comment: Optional description/comment for the storage credential
        metastore_id: ID of the metastore (optional, defaults to current)
        owner: Owner of the storage credential
        read_only: Whether the storage credential is read-only
        skip_validation: Whether to skip validation during creation
        force_destroy: Whether to force destroy on deletion
        force_update: Whether to force update on changes
        isolation_mode: Isolation mode
        access_connector_id: Azure access connector ID for managed identity authentication
    """
    name: str
    comment: Optional[str] = None
    metastore_id: Optional[str] = None
    owner: Optional[str] = None
    read_only: Optional[bool] = False
    skip_validation: Optional[bool] = False
    force_destroy: Optional[bool] = False
    force_update: Optional[bool] = False
    isolation_mode: Optional[str] = "ISOLATION_MODE_ISOLATED"
    access_connector_id: str

class ExternalLocation(BaseModel):
    """
    External location configuration.

    Attributes:
        name: Name of the external location
        url: Storage URL (e.g., abfss://container@storage.dfs.core.windows.net/path)
        credential_name: Name of the storage credential to use for access
        owner: Owner of the external location
        comment: Optional description/comment
        skip_validation: Whether to skip validation during creation
        fallback: Whether this is a fallback location
        read_only: Whether the location is read-only
        force_destroy: Whether to force destroy on deletion
        force_update: Whether to force update on changes
        isolation_mode: Isolation mode for the external location
    """
    name: str
    url: str
    credential_name: str
    owner: Optional[str] = None
    comment: Optional[str] = None
    skip_validation: Optional[bool] = False
    fallback: Optional[bool] = False
    read_only: Optional[bool] = False
    force_destroy: Optional[bool] = False
    force_update: Optional[bool] = False
    isolation_mode: Optional[str] = "ISOLATION_MODE_ISOLATED"

class Catalog(BaseModel):
    """
    Catalog configuration.

    Attributes:
        name: Name of the catalog
        storage_root: Optional storage location for managed tables
        provider_name: Provider name for federated catalogs
        share_name: Share name for catalogs created from delta sharing
        connection_name: Connection name for foreign catalogs
        owner: Owner of the catalog
        isolation_mode: Isolation mode (ISOLATED or OPEN)
        enable_predictive_optimization: Predictive optimization setting (INHERIT, ENABLE, DISABLE)
        comment: Optional description/comment
        properties: Custom properties for the catalog
        options: Custom options for the catalog
        force_destroy: Whether to force destroy on deletion
    """
    name: str
    storage_root: Optional[str] = None
    provider_name: Optional[str] = None
    share_name: Optional[str] = None
    connection_name: Optional[str] = None
    owner: Optional[str] = None
    isolation_mode: Optional[str] = "ISOLATED"
    enable_predictive_optimization: Optional[str] = "INHERIT"
    comment: Optional[str] = None
    properties: Optional[Dict[str, str]] = None
    options: Optional[Dict[str, str]] = None
    force_destroy: Optional[bool] = False

class Schema(BaseModel):
    """
    Schema configuration.

    Attributes:
        name: Name of the schema
        catalog_name: Name of the catalog
        storage_root: Optional storage location for managed tables in this schema
        owner: Owner of the schema
        comment: Optional description/comment
        properties: Custom properties for the schema
        enable_predictive_optimization: Predictive optimization setting (INHERIT, ENABLE, DISABLE)
        force_destroy: Whether to force destroy on deletion
    """
    name: str
    catalog_name: str
    storage_root: Optional[str] = None
    owner: Optional[str] = None
    comment: Optional[str] = None
    properties: Optional[Dict[str, str]] = None
    enable_predictive_optimization: Optional[str] = "INHERIT"
    force_destroy: Optional[bool] = False

class Volume(BaseModel):
    """
    Volume configuration.

    Attributes:
        name: Name of the volume
        catalog_name: Name of the parent catalog
        schema_name: Name of the parent schema
        volume_type: Type of volume (MANAGED or EXTERNAL)
        owner: Owner of the volume
        storage_location: Storage location for external volumes
        comment: Optional description/comment
    """
    name: str
    catalog_name: str
    schema_name: str
    volume_type: Optional[str] = "MANAGED"
    owner: Optional[str] = None
    storage_location: Optional[str] = None
    comment: Optional[str] = None

class Column(BaseModel):
    """
    Column configuration.

    Attributes:
        name: Name of the column
        type: Data type of the column (defaults to 'string')
        comment: Optional description/comment for the column
        nullable: Whether the column can contain NULL values
        identity: Identity column setting ('default' or 'always')
    """
    name: str
    type: Optional[str] = "string"
    comment: Optional[str] = None
    nullable: Optional[bool] = True
    identity: Optional[str] = None  # only "default" or "always"

class SQLTable(BaseModel):
    """
    SQL table configuration.

    Attributes:
        name: Name of the table
        catalog_name: Name of the parent catalog
        schema_name: Name of the parent schema
        table_type: Type of table (MANAGED, EXTERNAL, VIEW)
        comment: Optional description/comment
        owner: Owner of the table
        view_definition: SQL definition for views
        cluster_keys: List of columns to use for clustering
        partitions: List of columns to use for partitioning
        data_source_format: Data format (DELTA, PARQUET, etc.)
        storage_location: Storage location for external tables
        options: Table options
        properties: Custom properties for the table
        columns: List of column definitions
    """
    name: str
    catalog_name: str
    schema_name: str
    table_type: Optional[str] = "MANAGED"
    comment: Optional[str] = None
    owner: Optional[str] = None
    view_definition: Optional[str] = None
    cluster_keys: Optional[List[str]] = None
    partitions: Optional[List[str]] = None
    data_source_format: Optional[str] = None
    storage_location: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    properties: Optional[Dict[str, str]] = None
    columns: Optional[List[Column]] = None

class UcObjectsConfig(BaseModel):
    """
    Unity Catalog objects configuration.

    Attributes:
        storage_creds: List of storage credential configurations
        external_locations: List of external location configurations
        catalogs: List of catalog configurations
        schemas: List of schema configurations
        volumes: List of volume configurations
        sql_tables: List of SQL table configurations
    """
    storage_creds: Optional[List[StorageCredInfo]] = None
    external_locations: Optional[List[ExternalLocation]] = None
    catalogs: Optional[List[Catalog]] = None
    schemas: Optional[List[Schema]] = None
    volumes: Optional[List[Volume]] = None
    sql_tables: Optional[List[SQLTable]] = None

# Define Pydantic models for Delta Sharing
class Recipient(BaseModel):
    """
    Delta Sharing recipient configuration.

    Attributes:
        name: Name of the recipient
        recipient_sharing_id: Global metastore ID of the recipient
        comment: Optional description/comment for the recipient
    """
    name: str
    recipient_sharing_id: str
    comment: Optional[str] = ""

class ShareObject(BaseModel):
    """
    Object included in a Delta Sharing share.

    Attributes:
        type: Type of the shared object (TABLE, VIEW, etc.)
        name: Fully 3-level name of the shared object
        history_data_sharing_status: Whether to share historical data (ENABLED or DISABLED)
    """
    type: str
    name: str
    history_data_sharing_status: Optional[str] = "ENABLED"

class Share(BaseModel):
    """
    Delta Sharing share configuration.

    Attributes:
        name: Name of the share
        recipient_names: List of recipient names to grant access to this share
        internal_recipient_catalog_name: Name of catalog to create for internal recipients
        objects: List of objects (tables, views) to include in the share
        comment: Optional description/comment for the share
    """
    name: str
    recipient_names: Optional[List[str]] = []
    internal_recipient_catalog_name: Optional[str] = None
    objects: List[ShareObject]
    comment: Optional[str] = ""

class DeltaSharingConfig(BaseModel):
    """
    Delta Sharing configuration.

    Attributes:
        recipients: List of Delta Sharing recipient configurations
        shares: List of Delta Sharing share configurations
    """
    recipients: Optional[List[Recipient]] = None
    shares: Optional[List[Share]] = None

# Root configuration model
class RootConfig(BaseModel):
    """
    Root configuration model that encompasses all Unity Catalog configurations.

    Attributes:
        uc_objects_config: Unity Catalog objects configuration (catalogs, schemas, tables, etc.)
        delta_sharing_config: Delta Sharing configuration (recipients and shares)
        uc_object_grants_config: Grants configuration for Unity Catalog objects
    """
    uc_objects_config: Optional[UcObjectsConfig] = None
    delta_sharing_config: Optional[DeltaSharingConfig] = None
    uc_object_grants_config: Optional[UcObjectGrantsConfig] = None



def _validate_config(config):
    """
    Validate configuration structure using Pydantic models.

    Args:
        config (dict): Configuration dictionary to validate

    Returns:
        str or None: Error message if validation fails, None if successful

    Raises:
        ValidationError: If the configuration structure is invalid
    """
    try:
        RootConfig(**config)
        return None
    except ValidationError as e:
        _err_msg = f"Config structure validation failed: {str(e)}"
        return _err_msg
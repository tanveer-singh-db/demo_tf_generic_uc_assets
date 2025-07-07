from typing import List, Optional, Dict

from pydantic import BaseModel, ValidationError


# Define Pydantic models for Grants Configuration
class Grant(BaseModel):
    principals: List[str]
    permissions: List[str]

class CatalogGrant(BaseModel):
    name: str
    grants: List[Grant]

class SchemaGrant(BaseModel):
    name: str
    grants: List[Grant]

class ExternalLocationGrant(BaseModel):
    name: str
    grants: List[Grant]

class VolumeGrant(BaseModel):
    name: str  # Fully qualified: catalog.schema.volume
    grants: List[Grant]

class TableGrant(BaseModel):
    name: str  # Fully qualified: catalog.schema.table
    grants: List[Grant]

class FunctionGrant(BaseModel):
    name: str  # Fully qualified: catalog.schema.function
    grants: List[Grant]

class ModelGrant(BaseModel):
    name: str  # Fully qualified: catalog.schema.model
    grants: List[Grant]

class UcObjectGrantsConfig(BaseModel):
    catalogs: Optional[List[CatalogGrant]] = None
    schemas: Optional[List[SchemaGrant]] = None
    external_locations: Optional[List[ExternalLocationGrant]] = None
    volumes: Optional[List[VolumeGrant]] = None
    tables: Optional[List[TableGrant]] = None
    functions: Optional[List[FunctionGrant]] = None
    models: Optional[List[ModelGrant]] = None


class StorageCredInfo(BaseModel):
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
    name: str
    catalog_name: str
    storage_root: Optional[str] = None
    owner: Optional[str] = None
    comment: Optional[str] = None
    properties: Optional[Dict[str, str]] = None
    enable_predictive_optimization: Optional[str] = "INHERIT"
    force_destroy: Optional[bool] = False

class Volume(BaseModel):
    name: str
    catalog_name: str
    schema_name: str
    volume_type: Optional[str] = "MANAGED"
    owner: Optional[str] = None
    storage_location: Optional[str] = None
    comment: Optional[str] = None

class Column(BaseModel):
    name: str
    type: Optional[str] = "string"
    comment: Optional[str] = None
    nullable: Optional[bool] = True
    identity: Optional[str] = None  # only "default" or "always"

class SQLTable(BaseModel):
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
    storage_creds: Optional[List[StorageCredInfo]] = None
    external_locations: Optional[List[ExternalLocation]] = None
    catalogs: Optional[List[Catalog]] = None
    schemas: Optional[List[Schema]] = None
    volumes: Optional[List[Volume]] = None
    sql_tables: Optional[List[SQLTable]] = None

# Define Pydantic models for Delta Sharing
class Recipient(BaseModel):
    name: str
    recipient_sharing_id: str
    comment: Optional[str] = ""

class ShareObject(BaseModel):
    type: str
    name: str
    history_data_sharing_status: Optional[str] = "ENABLED"

class Share(BaseModel):
    name: str
    recipient_names: Optional[List[str]] = []
    internal_recipient_catalog_name: Optional[str] = None
    objects: List[ShareObject]
    comment: Optional[str] = ""

class DeltaSharingConfig(BaseModel):
    recipients: Optional[List[Recipient]] = None
    shares: Optional[List[Share]] = None

# Root configuration model
class RootConfig(BaseModel):
    uc_objects_config: Optional[UcObjectsConfig] = None
    delta_sharing_config: Optional[DeltaSharingConfig] = None
    uc_object_grants_config: Optional[UcObjectGrantsConfig] = None



def _validate_config(config):
    """Validate configuration structure using Pydantic models"""
    try:
        RootConfig(**config)
        return None
    except ValidationError as e:
        _err_msg = f"Config structure validation failed: {str(e)}"
        return _err_msg
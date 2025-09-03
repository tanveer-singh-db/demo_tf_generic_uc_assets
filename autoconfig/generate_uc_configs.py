from typing import Optional, List

import yaml
import re
from pathlib import Path

from autoconfig.common.logging_utils import get_log
from autoconfig.common.utils import get_exception

try:
    from databricks.sdk import WorkspaceClient
    DATABRICKS_SDK_AVAILABLE = True
except ImportError:
    DATABRICKS_SDK_AVAILABLE = False

class UCConfigGenerator:
    """
    Main generator for Unity Catalog configurations from meta templates.
    
    This class generates Unity Catalog configuration YAML files from meta templates,
    supporting variable substitution and dynamic user schema generation from Databricks groups.
    """
    def __init__(self,
                 bu:str,
                 sub_domain:str,
                 meta_config_root: str,
                 meta_file_name:str,
                 cloud_environment: str,
                 region: str,
                 workspace_info: str,
                 subscription_id: str,
                 databricks_workspace_url: str,
                 output_root: Optional[str] =None,
                 app_name: Optional[str] =None,
                 generate_user_schemas: bool = False,
                 user_groups: Optional[List[str]] = None,
                 user_schema_template: str = "<user_name>_schema",
                 databricks_token: Optional[str] = None
                 ):
        """
        Initialize generator with parameters and load meta configuration.
        
        Args:
            bu: Business unit name for config generation
            sub_domain: Subdomain name for config generation
            meta_config_root: Path to directory containing meta configuration templates
            meta_file_name: Name of the meta template file to use
            cloud_environment: Cloud environment (dev, qa, prod)
            region: Azure region (e.g., westeurope, southeastasia)
            workspace_info: Workspace identifier for config path structure
            subscription_id: Azure subscription ID
            databricks_workspace_url: Databricks workspace URL
            output_root: Optional root directory for generated files (defaults to current directory)
            app_name: Optional application name for multi-app deployments
            generate_user_schemas: Whether to generate user schemas from Databricks groups
            user_groups: List of Databricks group names to read users from
            user_schema_template: Template string for user schema names (supports <user_name> variable)
            databricks_token: Databricks API token for group member retrieval
        """
        self.log = get_log("generator")
        self.bu = bu
        self.sub_domain = sub_domain
        self.meta_config_root = Path(meta_config_root)
        self.meta_file_name = meta_file_name
        self.cloud_environment = cloud_environment
        self.region = region
        self.workspace_info = workspace_info
        self.subscription_id = subscription_id
        self.databricks_workspace_url = databricks_workspace_url
        self.app_name = app_name
        self.output_root = Path(output_root)
        self.generate_user_schemas_flag = generate_user_schemas
        self.user_groups = user_groups or []
        self.user_schema_template = user_schema_template
        self.databricks_token = databricks_token
        self.meta = self.load_meta_config()
        self.ctx = self.build_context()
        self.uc_objects = {}
        self.uc_grants = {}
        self.tfvars = {}

    def load_meta_config(self):
        """Load and merge meta configuration from YAML file."""
        meta_file_path = self.meta_config_root / self.meta_file_name
        if not meta_file_path.exists():
            raise FileNotFoundError(f"Meta file not found: {meta_file_path}")
        try:
            self.log.info(f"Loading meta config from {meta_file_path}")

            full_meta = yaml.safe_load(meta_file_path.read_text()) or {}
            base_config = full_meta.get("base") or {}
            env_overrides = full_meta.get(self.cloud_environment) or {}

            if not isinstance(base_config, dict) or not isinstance(env_overrides, dict):
                raise TypeError("Both 'base' and environment override sections must be dictionaries")

            merged_config = {**base_config, **env_overrides}
            return merged_config
        except:
            e = get_exception()
            self.log.error(e)
            raise Exception(e)

    def render_string(self, template: str, context: dict) -> str:
        """Replace template variables in strings with context values."""
        return re.sub(r"<([^>]+)>", lambda m: str(context.get(m.group(1), m.group(0))), template)

    def sanitize_user_name(self, user_name: str) -> str:
        """Convert user name/email to valid Databricks schema name"""
        # Remove domain from email addresses
        if "@" in user_name:
            user_name = user_name.split("@")[0]

        # Replace special characters with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", user_name)

        # Ensure it starts with letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"user_{sanitized}"

        # Convert to lowercase for consistency
        return sanitized.lower()

    def fetch_all_group_members(self) -> List[str]:
        """Fetch members from all configured Databricks groups"""
        if not DATABRICKS_SDK_AVAILABLE:
            self.log.warning("Databricks SDK not available. Cannot fetch group members.")
            return []

        if not self.databricks_token:
            self.log.warning("No Databricks token provided. Cannot fetch group members.")
            return []

        if not self.user_groups:
            self.log.info("No user groups configured.")
            return []

        all_users = set()

        try:
            client = WorkspaceClient(
                host=self.databricks_workspace_url,
                token=self.databricks_token
            )

            for group_name in self.user_groups:
                try:
                    self.log.info(f"Fetching members from group: {group_name}")

                    # List all groups and find the one we want
                    groups = list(client.groups.list(filter=f'displayName eq "{group_name}"'))

                    if not groups:
                        self.log.warning(f"Group '{group_name}' not found")
                        continue

                    group = groups[0]

                    # Get group details including members
                    group_details = client.groups.get(group.id)

                    if group_details.members:
                        total_members = len(group_details.members)
                        user_count = 0

                        for member in group_details.members:
                            # Check if member is a user by examining the ref field
                            if hasattr(member, 'ref') and member.ref:
                                if not member.ref.startswith('Users/'):
                                    member_type = member.ref.split('/')[0] if '/' in member.ref else 'Unknown'
                                    self.log.debug(f"Skipping {member_type} member: {member.display or member.value} (ref: {member.ref})")
                                    continue
                            else:
                                # Fallback: Skip members without ref field
                                self.log.debug(f"Skipping member without ref field: {member.display or member.value}")
                                continue

                            # Process user-type members
                            if member.display and member.value:
                                # Use display name if available, otherwise use value (usually email)
                                user_identifier = member.display or member.value
                                all_users.add(user_identifier)
                                user_count += 1
                                self.log.debug(f"Added user: {user_identifier} (ref: {member.ref})")

                    self.log.info(f"Found {total_members} total members in group '{group_name}', processed {user_count} users")

                except Exception as e:
                    self.log.error(f"Error fetching members from group '{group_name}': {str(e)}")
                    continue

            self.log.info(f"Total unique users found across all groups: {len(all_users)}")
            return list(all_users)

        except Exception as e:
            self.log.error(f"Error connecting to Databricks: {str(e)}")
            return []

    def build_context(self):
        """Build context dictionary with all template variables and configurations."""
        prefix = "ts42"  # or make this another CLI arg if needed
        ctx = {
            "prefix": prefix,
            "bu": self.bu,
            "subdomain": self.sub_domain,
            "env": self.cloud_environment,
            "region": self.region,
            "workspace_info": self.workspace_info,
            "subscription_id": self.subscription_id,
            "databricks_workspace_url": self.databricks_workspace_url,
        }
        if self.app_name:
            ctx["app_name"] = self.app_name

        # expand any templated strings in meta
        for key in [
            "storage_account",
            "catalog_name",
            "schema_name",
            "catalog_location",
            "schema_location",
            "catalog_admin_group",
            "user_schema_location",
        ]:
            if key in self.meta:
                ctx[key] = self.render_string(self.meta[key], ctx)

        # expand lists like catalog_user_groups, schema_user_groups
        for list_key in ["catalog_user_groups", "schema_user_groups"]:
            if list_key in self.meta:
                ctx[list_key] = [self.render_string(item, ctx) for item in self.meta[list_key]]

        # copy through static permissions
        ctx["catalog_admin_grants"] = self.meta.get("catalog_admin_grants", [])
        ctx["schema_read_only_grants"] = self.meta.get("schema_read_only_grants", [])
        ctx["schema_read_write_grants"] = self.meta.get("schema_read_write_grants", [])

        # flag for medallion tier generation
        ctx["generate_medallion"] = self.meta.get("generate_medallion", True)

        # user schema configuration from meta
        ctx["generate_user_schemas_flag"] = self.meta.get("generate_user_schemas", self.generate_user_schemas_flag)
        ctx["user_groups"] = self.meta.get("user_groups", self.user_groups)
        ctx["user_schema_template"] = self.meta.get("user_schema_template", self.user_schema_template)

        return ctx

    def generate_user_schemas(self) -> List[dict]:
        """Generate schema configurations for all users from configured groups"""
        if not self.generate_user_schemas_flag:
            return []

        users = self.fetch_all_group_members()
        if not users:
            self.log.info("No users found from configured groups")
            return []

        user_schemas = []
        user_external_locations = []

        for user in users:
            sanitized_name = self.sanitize_user_name(user)

            # Create user-specific context for template rendering
            user_ctx = {**self.ctx, "user_name": sanitized_name}

            # Render schema name from template
            schema_name = self.render_string(self.user_schema_template, user_ctx)

            # Create user schema configuration
            user_schema = {
                "name": schema_name,
                "catalog_name": self.ctx["catalog_name"],
                "comment": f"Personal schema for user {user}",
                "owner": user if "@" in user else None  # Use email as owner if available
            }

            # Add storage_root if we have a location template in meta config
            if "user_schema_location" in self.meta:
                schema_location = self.render_string(self.meta["user_schema_location"], user_ctx)
                user_schema["storage_root"] = f"abfss://{schema_location}.dfs.core.windows.net/"

            user_schemas.append(user_schema)

            # Create corresponding external location if storage_root is defined
            if "storage_root" in user_schema:
                user_external_locations.append({
                    "name": f"{schema_name}@{self.ctx.get('storage_account', 'storage')}",
                    "url": user_schema["storage_root"],
                    "credential_name": f"{self.ctx['catalog_name']}_storage_creds",
                    "comment": f"External location for {user} personal schema"
                })

        self.log.info(f"Generated {len(user_schemas)} user schemas")

        # Store external locations for later use in generate_uc_objects
        self._user_external_locations = user_external_locations

        return user_schemas

    def generate_uc_objects(self):
        """Generate Unity Catalog objects configuration (catalogs, schemas, external locations)."""
        tiers = ["bronze", "silver", "gold"] if self.ctx.get("generate_medallion") else []
        tiers.append("mlassets")

        schemas = []
        external_locations = []

        # Generate tier-based schemas (existing logic)
        for tier in tiers:
            self.ctx["data_maturity"] = tier
            schema_name = self.render_string(self.meta["schema_name"], self.ctx)
            schema_location = self.render_string(self.meta["schema_location"], {**self.ctx, "schema_name": schema_name})

            schemas.append({
                "name": schema_name,
                "catalog_name": self.ctx["catalog_name"],
                "location": f"abfss://{schema_location}.dfs.core.windows.net/"
            })

            external_locations.append({
                "name": f"{schema_name}@{self.ctx['storage_account']}",
                "location": f"abfss://{schema_name}@{self.ctx['storage_account']}.dfs.core.windows.net/",
                "credential_name": f"{self.ctx['catalog_name']}_storage_creds"
            })

        # Generate user-based schemas
        user_schemas = self.generate_user_schemas()
        schemas.extend(user_schemas)

        # Add user external locations if they were generated
        if hasattr(self, '_user_external_locations'):
            external_locations.extend(self._user_external_locations)

        return {
            "options": {
                "create_storage_creds": True,
                "create_external_locations": True,
                "create_catalogs": True,
                "create_schemas": True
            },
            "storage_creds": [{
                "name": f"{self.ctx['catalog_name']}_storage_creds",
                "access_connector_id": f"/subscriptions/{self.ctx['subscription_id']}/resourceGroups/<resource-group>/providers/Microsoft.Databricks/accessConnectors/<connector-name>"
            }],
            "external_locations": external_locations,
            "catalogs": [{
                "name": self.ctx["catalog_name"],
                "location": f"abfss://{self.ctx['catalog_location']}.dfs.core.windows.net/",
                "owner": self.ctx["catalog_admin_group"],
                "comment": f"Catalog for {self.ctx['bu']} {self.ctx['subdomain']} {self.ctx['env']}"
            }],
            "schemas": schemas
        }

    def generate_uc_grants(self):
        """Generate access grants configuration for catalogs and schemas."""
        tiers = ["bronze", "silver", "gold"] if self.ctx.get("generate_medallion") else []
        tiers.append("mlassets")

        schemas = []
        for tier in tiers:
            self.ctx["data_maturity"] = tier
            schema_name = self.render_string(self.meta["schema_name"], self.ctx)
            fqn = f"{self.ctx['catalog_name']}.{schema_name}"
            grants = []
            for principal in self.ctx.get("schema_user_groups", []):
                perms = (
                    self.ctx["schema_read_write_grants"] if "rw" in principal else self.ctx["schema_read_only_grants"]
                )
                grants.append({"principal": principal, "permissions": perms})
            schemas.append({"name": fqn, "grants": grants})

        return {
            "catalogs": [{
                "name": self.ctx["catalog_name"],
                "grants": [{
                    "principal": self.ctx["catalog_admin_group"],
                    "permissions": self.ctx["catalog_admin_grants"]
                }] + [
                              {"principal": g, "permissions": ["USE_CATALOG"]} for g in
                              self.ctx.get("catalog_user_groups", [])
                          ]
            }],
            "schemas": schemas
        }

    def generate_tfvars(self):
        """Generate Terraform variables file content."""
        return {
            "deployment_subscription_id": self.ctx["subscription_id"],
            "databricks_workspace_url": self.ctx["databricks_workspace_url"],
            "deployment_tenant_id": "<tenant-id>",
            "databricks_account_id": "<account-id>",
            "uc_objects_config_file": "uc_objects.yml",
            "uc_object_grants_config_file": "uc_object_grants.yml",
            "cloudEnvironment": self.ctx["env"],
            "region": self.ctx["region"],
            "workspaceInfo": self.ctx["workspace_info"]
        }

    def write_output_files(self):
        """Write all generated configurations to output files."""
        out_path = self.output_root / self.ctx["env"] / self.ctx["region"] / self.ctx["workspace_info"] /"test"
        out_path.mkdir(parents=True, exist_ok=True)
        (out_path / "uc_objects.yml").write_text(yaml.dump(self.uc_objects, sort_keys=False))
        (out_path / "uc_object_grants.yml").write_text(yaml.dump(self.uc_grants, sort_keys=False))
        (out_path / "terraform.tfvars").write_text(
            "\n".join(f'{k} = "{v}"' for k, v in self.tfvars.items())
        )
        print(f"✅ Files written to {out_path}")

    def run(self):
        """Execute the complete generation workflow."""
        self.uc_objects = self.generate_uc_objects()
        self.uc_grants = self.generate_uc_grants()
        self.tfvars = self.generate_tfvars()
        self.write_output_files()

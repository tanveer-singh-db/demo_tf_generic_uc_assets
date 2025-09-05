"""Unity Catalog configuration generator CLI tool.

This script generates Unity Catalog configurations (catalogs, schemas, grants, etc.)
from meta templates for Databricks workspaces.
"""

import argparse
from pathlib import Path

from autoconfig.generate_uc_configs import UCConfigGenerator

# Project configuration defaults
PROJECT_ROOT = Path(__file__).parent
DEFAULT_META_CONFIG_ROOT = str(PROJECT_ROOT / "meta_configs")
DEFAULT_META_FILE_NAME = "meta_bu_subdomain_app_template.yml"
DEFAULT_OUTPUT_ROOT = str(PROJECT_ROOT)
DEFAULT_REGION = "westeurope"
DEFAULT_SUBSCRIPTION_ID = ""
DEFAULT_WORKSPACE_URL = ""

# Command line argument parser setup
parser = argparse.ArgumentParser(description="Generate Unity Catalog configurations from meta templates")

# Required arguments
parser.add_argument("--bu", type=str, required=True, help="Business unit name (required)")
parser.add_argument("--sub_domain", type=str, required=True, help="Subdomain name (required)")
parser.add_argument("--workspace_info", required=True, type=str, help="Unique workspace ID, e.g. '2178' (required)")

# Optional configuration arguments
parser.add_argument("--app_name", type=str, default=None, help="Application name for multi-app deployments")
parser.add_argument("--meta_config_root", default=DEFAULT_META_CONFIG_ROOT, help="Path to meta_configs directory")
parser.add_argument("--meta_file_name", default=DEFAULT_META_FILE_NAME, help="Name of the meta template file")
parser.add_argument("--cloud_environment", default="dev", type=str, help="Cloud environment (dev, stg, prod)")
parser.add_argument("--region", default=DEFAULT_REGION, type=str, help="Azure region (e.g. westeurope, southeastasia)")
parser.add_argument("--subscription_id", default=DEFAULT_SUBSCRIPTION_ID, help="Azure Subscription ID")
parser.add_argument("--databricks_workspace_url", default=DEFAULT_WORKSPACE_URL, help="Databricks Workspace URL")
parser.add_argument("--output_root", default=DEFAULT_OUTPUT_ROOT, help="Root folder to write generated files")

# User schema generation arguments (optional feature)
parser.add_argument("--generate_user_schemas", action="store_true", help="Enable generation of user-based schemas from Databricks groups")
parser.add_argument("--user_groups", nargs="*", default=[], help="List of Databricks groups to read members from (space-separated)")
parser.add_argument("--user_schema_template", default="<user_name>_schema", help="Template for user schema names")
parser.add_argument("--databricks_token", default="", help="Databricks authentication token for API access (required for user schema generation)")

def main():
    """Main entry point for the configuration generator."""
    # Parse command line arguments
    args = parser.parse_args()
    
    # Create and configure the UC config generator
    uccfg = UCConfigGenerator(
        # Core identification parameters
        bu=args.bu,
        sub_domain=args.sub_domain,
        workspace_info=args.workspace_info,
        
        # Template and environment configuration
        meta_config_root=args.meta_config_root,
        meta_file_name=args.meta_file_name,
        cloud_environment=args.cloud_environment,
        region=args.region,
        
        # Azure and Databricks configuration
        subscription_id=args.subscription_id,
        databricks_workspace_url=args.databricks_workspace_url,
        
        # Output configuration
        output_root=args.output_root,
        app_name=args.app_name,
        
        # User schema generation options
        generate_user_schemas=args.generate_user_schemas,
        user_groups=args.user_groups,
        user_schema_template=args.user_schema_template,
        databricks_token=args.databricks_token or None
    )
    
    # Execute the configuration generation workflow
    uccfg.run()

if __name__ == '__main__':
    main()
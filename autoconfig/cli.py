import argparse
import os
import sys
import yaml
from .config_validator import ConfigValidator
from databricks.sdk import WorkspaceClient


def main():
    parser = argparse.ArgumentParser(description='Validate Unity Catalog configuration')
    parser.add_argument('config', type=str, help='Path to YAML configuration file')
    parser.add_argument("")
    args = parser.parse_args()

    try:
        with open(args.config) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading config file: {str(e)}")
        sys.exit(2)

    # Get environment variables
    required_envs = [
        'AZURE_SUBSCRIPTION_ID',
        'DATABRICKS_HOST',
        'DATABRICKS_TOKEN'
    ]

    missing = [env for env in required_envs if env not in os.environ]
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        sys.exit(3)

    try:
        # Initialize clients
        db_client = WorkspaceClient(
            host=os.environ['DATABRICKS_HOST'],
            token=os.environ['DATABRICKS_TOKEN']
        )

        # Run validation
        validator = ConfigValidator(
            config,
            os.environ['AZURE_SUBSCRIPTION_ID'],
            db_client
        )
        errors = validator.validate()

        if errors:
            print("❌ Validation errors found:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)
        else:
            print("✅ All checks passed successfully")
            sys.exit(0)

    except Exception as e:
        print(f"🔥 Validation failed with unexpected error: {str(e)}")
        sys.exit(4)


if __name__ == "__main__":
    main()
"""
Unity Catalog Configuration Validation CLI Tool

This script provides a command-line interface for validating Unity Catalog configurations
against Azure resources and Databricks workspace settings.
"""
import argparse
import json
from argparse import ArgumentParser

from autoconfig.config_validator import ConfigValidator

parser = argparse.ArgumentParser(description='Validate Unity Catalog configuration')
parser.add_argument('--config_dir', type=str,required=True, help='Directory Path where .yml/.yaml configuration files are located')
parser.add_argument("--workspace_url",type=str,required=True, help = "Databricks workspace URL, i.e. https://adb-xxx.x.azuredatabricks.net" )
parser.add_argument("--subscription_id",type=str,required=True, help = "Azure subscription ID, i.e. xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" )



def main():
    args = parser.parse_args()

    cvl = ConfigValidator(config_dir = args.config_dir,
                          subscription_id = args.subscription_id,
                          workspace_url = args.workspace_url
                        )
    l_errors = cvl.validate()
    if l_errors:
        e = Exception("Error encountered during validation of configs: "+json.dumps(l_errors, indent=4))
        raise e


if __name__ == "__main__":
    main()
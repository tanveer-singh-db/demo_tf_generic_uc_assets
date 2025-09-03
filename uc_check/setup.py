from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uc-config-validator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Unity Catalog Configuration Validator for Azure Databricks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/uc-config-validator",
    packages=find_packages(),
    install_requires=[
        "databricks-sdk>=0.15.0",
        "azure-identity>=1.15.0",
        "azure-mgmt-storage>=21.1.0",
        "pydantic>=2.0",
        "pyyaml>=6.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "validate-uc-config=uc_config_validator.cli:main",
        ],
    },
    keywords="databricks unity-catalog azure validation",
    project_urls={
        "Documentation": "https://github.com/your-org/uc-config-validator/wiki",
        "Source": "https://github.com/your-org/uc-config-validator",
        "Tracker": "https://github.com/your-org/uc-config-validator/issues",
    },
)
# perisher
Create custom outputs from Microsoft Azure infrastructure via the Azure CLI

# description


# requirements
Docker 17.X

# main configuration
The following environment variables can be used for configuration (see `modules.environment`):
1. AZURE_USERNAME - The usename to use when logging in
2. AZURE_TENANT_ID - The tenant id to use when logging in
3. AZURE_CERTIFICATE_PATH - The path to the certificated file to use when logging in
4. AZURE_ACCOUNT_ID - The account id to use when logged in
5. DEBUG - Set it to anything to enable debug logging
6. RESOURCE_GROUP_TAG_NAME - What tag name to look for when filtering resource groups (don't set for all groups)
7. RESOURCE_GROUP_TAG_VALUE - What the value of the above given tag should be to be selected (only used if RESOURCE_GROUP_TAG_NAME is set)
8. SKIP_AZURE - Used during development and test. Skips Azure CLI calls and generates a test dataset.

# exporter configuration
The following environment variables can be used to configure the bundled exporters:
--

# volumes
The following Docker volumes should be mounted for the program to work:
1. local/cert/path/file.pem:[AZURE_CERTIFICATE_PATH] - The certificate file used to autheticate with Azure
2. local/export/dir:/exports - The directory to use for file exports

# to run
1. `docker build -t perisher .`
2. `docker run -e ENVS=TO_USE -e GOES=HERE -v local/cert/path/:path/from/AZURE_CERTIFICATE_PATH perisher`
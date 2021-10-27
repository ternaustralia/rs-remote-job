FLASK_APP=resource_server
FLASK_ENV=development

RESOURCE_SERVER_SETTINGS=development.cfg


KEY_SIGNING_BASE_URL_ENV=
# SLURM master node
MASTER_NODE_HOST_ENV=
MASTER_NODE_USER_ENV=
MASTER_NODE_PORT_ENV=
CMD_JSON_FILE_ABS_PATH_ENV=

# TODO: move this into development.cfg?
#       it's secrets ... would be much better to fake it away somehow
RESOURCE_SERVER_OIDC_DISCOVERY_URL='https://auth-test.tern.org.au/auth/realms/local/.well-known/openid-configuration'
RESOURCE_SERVER_OIDC_CLIENT_ID=dst
RESOURCE_SERVER_OIDC_CLIENT_SECRET=
RESOURCE_SERVER_OIDC_USE_REFRESH_TOKEN=True
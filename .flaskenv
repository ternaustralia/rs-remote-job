FLASK_APP=resource_server
FLASK_ENV=development

RESOURCE_SERVER_SETTINGS=development.cfg

KEY_SIGNING_BASE_URL_ENV=http://127.0.0.1:5000/
 # SLURM master node
MASTER_NODE_HOST_ENV=172.18.0.3
MASTER_NODE_USER_ENV=ec2-user
MASTER_NODE_PORT_ENV=22


# TODO: move this into development.cfg?
#       it's secrets ... would be much better to fake it away somehow
RESOURCE_SERVER_OIDC_DISCOVERY_URL='https://auth-test.tern.org.au/auth/realms/local/.well-known/openid-configuration'
RESOURCE_SERVER_OIDC_CLIENT_ID=dst
RESOURCE_SERVER_OIDC_CLIENT_SECRET=
RESOURCE_SERVER_OIDC_USE_REFRESH_TOKEN=True
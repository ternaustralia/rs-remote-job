FLASK_APP=resource_server
FLASK_ENV=development

SSH_CERT_SERVICE_SETTINGS=development.cfg

MASTER_PRIVATE_KEY_PATH_ENV=
MASTER_KEY_PASSPHRASE_ENV=

# TODO: move this into development.cfg?
#       it's secrets ... would be much better to fake it away somehow
SSH_CERT_SERVICE_OIDC_DISCOVERY_URL=
SSH_CERT_SERVICE_OIDC_CLIENT_ID=
SSH_CERT_SERVICE_OIDC_CLIENT_SECRET=
SSH_CERT_SERVICE_OIDC_USE_REFRESH_TOKEN=
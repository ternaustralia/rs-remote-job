FLASK_APP=resource-server
FLASK_ENV=development

RESOURCE-SERVER_SETTINGS=development.cfg

# TODO: move this into development.cfg?
#       it's secrets ... would be much better to fake it away somehow
RESOURCE-SERVER_OIDC_DISCOVERY_URL='https://auth-test.tern.org.au/auth/realms/local/.well-known/openid-configuration'
RESOURCE-SERVER_OIDC_CLIENT_ID=dst
RESOURCE-SERVER_OIDC_CLIENT_SECRET=
RESOURCE-SERVER_OIDC_USE_REFRESH_TOKEN=True
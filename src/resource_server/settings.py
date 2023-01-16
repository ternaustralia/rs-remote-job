# Default settings
#
# This file is read before all other configuration sources
#
# The config file for the supported commands
from pathlib import Path

# Path to config file
CMD_PATH_FILE = str(Path.cwd() / "config/config.json")

# Put them in the parameters section in config.json??
# URL to the SSH cert service
SSH_KEYSIGN_BASE_URL=None
# The claim's principal; this is set to user's LDAP username in keycloak
SSH_PRINCIPAL_CLAIM='coesra_uname'
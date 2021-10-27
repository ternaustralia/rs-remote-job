# Default settings
#
# This file is read before all other configuration sources
#

import os
# This is the base url for the signing api 
BASE_URL = os.environ["KEY_SIGNING_BASE_URL_ENV"] + "/api/v1.0"

# SLURM master node
MASTER_NODE_HOST = os.environ["MASTER_NODE_HOST_ENV"]
MASTER_NODE_USER = os.environ["MASTER_NODE_USER_ENV"]
MASTER_NODE_PORT = os.environ["MASTER_NODE_PORT_ENV"]

COMMANDS_JSON_FILE = os.environ["CMD_JSON_FILE_ABS_PATH_ENV"]


import os
# This is the base url for the signing api 
BASE_URL = os.environ.get('MASTER_BASE_URL', 'http://127.0.0.1:5000') +'/api/v1.0'
# SLURM master node
MASTER_NODE_HOST = os.environ.get('MASTER_NODE_HOST')
MASTER_NODE_USER = os.environ.get('MASTER_NODE_USER')
MASTER_NODE_PORT = os.environ.get('MASTER_NODE_PORT')

COMMANDS_JSON_FILE = 'utils/commands.json'

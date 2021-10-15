import json
from typing import Dict
import paramiko
from paramiko.ssh_exception import SSHException

from constants import MASTER_NODE_HOST, MASTER_NODE_PORT, MASTER_NODE_USER, COMMANDS_JSON_FILE


def paramiko_stablish_connection(file, password: str = ''):
    """ User paramiko to stablish a connection to the master node
        Parameters
        -------------
        file: obj_file
            file that storage the privatekey
        password: str
            Optional password to load the private key

        Return
        -------------
        ssh
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()

    try:
        ssh_key = paramiko.RSAKey.from_private_key(file_obj=file, password=password)
    except SSHException: 
        # Request a new ssh_key certificate
        raise SSHException

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
            hostname=MASTER_NODE_HOST,
            username=MASTER_NODE_USER,
            port=MASTER_NODE_PORT,
            pkey=ssh_key
           )

    return ssh

def read_json_file() -> Dict[str, str]:
    """ Read JSON file that stores the full list of commands to be execute

        Return
        -------------
        json_data: Dict[str,str]
    """

    json_data = dict()
    with open(COMMANDS_JSON_FILE) as json_file:
        json_data = json.load(json_file)

    return json_data

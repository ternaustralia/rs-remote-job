import json
import paramiko
import tempfile

from jsonschema import validate
from typing import Dict
from resource_server.utils.signing_api import get_keys
from resource_server.settings import (
    MASTER_NODE_HOST,
    MASTER_NODE_PORT,
    MASTER_NODE_USER,
    COMMANDS_JSON_FILE,
    COMMANDS_JSON_SCHEMA
)



def paramiko_establish_connection():
    """ User paramiko to stablish a connection to the master node
        Parameters
        -------------
        Return
        -------------
        ssh
    """
    ssh = paramiko.SSHClient()
    keys = get_keys()

    # Create temporary dicrectory and storage the keys there
    with tempfile.TemporaryDirectory() as tmp_dir:
        keys_path = f"{tmp_dir}/private_key"
        tmp_public = open(f"{keys_path}.pub", "w")
        tmp_private = open(f"{keys_path}", "w")
        tmp_cert = open(f"{keys_path}-cert.pub", "w")
        tmp_public.write(keys["public_key"])
        tmp_private.write(keys["private_key"])
        tmp_cert.write(keys["cert_key"])
        tmp_public.close()
        tmp_private.close()
        tmp_cert.close()
        ssh_key = paramiko.RSAKey.from_private_key_file(keys_path)
        ssh_key.load_certificate(f"{keys_path}-cert.pub")

    # TODO: note, that we should use host key verification in some way.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
            hostname=MASTER_NODE_HOST,
            username=MASTER_NODE_USER,
            port=MASTER_NODE_PORT,
            pkey=ssh_key,
            look_for_keys=False
           )

    return ssh

def read_json_file() -> Dict[str, str]:
    """ Read JSON file that stores the full list of commands to be execute
        Return
        -------------
        json_data: Dict[str,str]
    """

    schema = dict()
    with open(COMMANDS_JSON_SCHEMA) as json_file:
        schema = json.load(json_file)

    instance = dict()
    with open(COMMANDS_JSON_FILE) as json_file:
        instance = json.load(json_file)

    validate(instance=instance, schema=schema)

    return instance
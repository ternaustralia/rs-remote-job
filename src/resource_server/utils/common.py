import importlib
try:
    from importlib.resources import files as pkg_files
except ImportError:
    from importlib_resources import files as pkg_files
import io
import json
import paramiko

from jsonschema import validate
from typing import Dict
from resource_server.utils.signing_api import get_keys


# TODO: host and port should come from cmds_config?
def paramiko_establish_connection(user, host, port=22):
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
    ssh_key = paramiko.RSAKey.from_private_key(io.StringIO(keys['private_key']))
    ssh_key.load_certificate(keys['cert_key'])

    # TODO: note, that we should use host key verification in some way.
    #       does AutoAddPolicy add to ~/.known_hosts ? or just an in memory?
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=host,
        username=user,
        port=port,
        pkey=ssh_key,
        look_for_keys=False
    )

    return ssh

def read_json_file(cmd_config) -> Dict[str, str]:
    """ Read JSON file that stores the full list of commands to be execute
        Return
        -------------
        json_data: Dict[str,str]
    """

    schema = dict()
    with (pkg_files(importlib.util.find_spec(__name__).parent) / "config.schema.json").open("r") as json_file:
        schema = json.load(json_file)

    instance = dict()
    with open(cmd_config) as json_file:
        instance = json.load(json_file)

    validate(instance=instance, schema=schema)

    return instance

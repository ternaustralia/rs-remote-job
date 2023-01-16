import io
import json
import paramiko
import importlib

from typing import Dict
from jsonschema import validate
from resource_server.utils.signing_api import get_keys

try:
    from importlib.resources import files as pkg_files
except ImportError:
    from importlib_resources import files as pkg_files


def paramiko_establish_connection(base_url: str, user: str, host: str, port: int, headers: Dict) -> paramiko.SSHClient:
    """ User paramiko to stablish a connection to the master node
        Parameters
        -------------
        Return
        -------------
        ssh
    """
    ssh = paramiko.SSHClient()

    # Call ssh-cert-service to generate key-pairs and associated cert-key
    keys = get_keys(base_url, headers)

    # Create temporary dicrectory and storage the keys there
    # TODO: support other than RSA key
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
#        key_filename=key['cert_key'],
        look_for_keys=False
    )
    return ssh

def validate_schema(path_file: str) -> Dict[str, any]:
    """ Load the command configuration JSON file and validate using the schema validator

        Parameters
        -------------
        path_file: str
            path to the command JSON configuration file
        Return
        -------------
        instance: dict

    """

    with (pkg_files(importlib.util.find_spec(__name__).parent) / "config.schema.json").open("r") as schema_file:
        schema = json.load(schema_file)

    with open(path_file) as path_instance:
        instance = json.load(path_instance)

    validate(instance=instance,schema=schema)

    return instance
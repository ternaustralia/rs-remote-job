import paramiko
import pytest
from resource_server.utils.common import paramiko_establish_connection 
from resource_server.utils.cmd import get_command


def test_paramiko_establish_connection(ssh_server, mock_post_request, base_url, cmds_path_config, test_command):
    """ Check if paramiko can connect with the host """

    command = get_command(test_command, dict(), cmds_path_config)
    command["port"] = ssh_server.port
    
    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"], dict())
    assert isinstance(ssh, paramiko.SSHClient)
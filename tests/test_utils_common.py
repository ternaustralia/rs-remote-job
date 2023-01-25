import paramiko
import pytest
from resource_server.utils.common import paramiko_establish_connection 
from resource_server.utils.cmd import get_command


def test_paramiko_establish_connection(ssh_server, mock_post_request, base_url, command_test_config, test_command):
    """ Check if paramiko can connect with the host """

    command = get_command(test_command, dict(), command_test_config)
    
    ssh = paramiko_establish_connection(base_url, "user", "localhost", ssh_server.port)
    assert isinstance(ssh, paramiko.SSHClient)
import paramiko

from resource_server.utils.common import paramiko_establish_connection, read_json_file


def test_read_json_file(cmds_config):
    """ Test function that reads a json file """
    json_data = read_json_file(cmds_config)

    assert isinstance(json_data, dict)
    assert json_data.get('endpoints') is not None


def test_paramiko_stablish_connection(ssh_server, mock_ssh_cert_service):
    """ Check if paramiko can connect with the host """

    ssh = paramiko_establish_connection('user', '127.0.0.1', ssh_server.port)
    assert isinstance(ssh, paramiko.SSHClient)

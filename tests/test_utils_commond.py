import paramiko

from resource_server.utils.common import paramiko_establish_connection, validate_schema


def test_validate_schema(cmds_path_config):
    """ Test function that reads a json file """
    json_data = validate_schema(cmds_path_config)

    assert isinstance(json_data, dict)
    assert json_data.get('endpoints') is not None


def test_paramiko_stablish_connection(ssh_server, mock_ssh_cert_service):
    """ Check if paramiko can connect with the host """

    ssh = paramiko_establish_connection('user', '127.0.0.1', ssh_server.port)
    assert isinstance(ssh, paramiko.SSHClient)

import paramiko
from paramiko import ssh_exception

from resource_server.utils.common import paramiko_establish_connection, validate_schema, create_request_param_to_config
from resource_server.utils.cmd import load_template_values


def test_validate_schema(cmds_path_config):
    """ Test function that reads a json file """
    json_data = validate_schema(cmds_path_config)

    assert isinstance(json_data, dict)
    assert json_data.get('endpoints') is not None


def test_validate_globals_schema(cmds_path_config):
    """ Test that the template loads the global params but it gets overwrited with the local params"""
    command = load_template_values(validate_schema(cmds_path_config), "test_globals", [])

    assert isinstance(command, dict)
    assert command["port"] == "5522"
    assert command["exec"]["command"] == "different_host_name /usr/bin/scancel /usr/bin/squeue"


def test_paramiko_stablish_connection(ssh_server, mock_post_request, base_url, cmds_path_config, test_command):
    """ Check if paramiko can connect with the host """

    command = load_template_values(validate_schema(cmds_path_config), test_command, [])
    command["port"] = ssh_server.port

    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"], dict())
    assert isinstance(ssh, paramiko.SSHClient)


def test_paramiko_fail_connection(ssh_server, mock_post_request, base_url, cmds_path_config):
    """ Check that paramiko is unable to connect with the default port """

    command = load_template_values(validate_schema(cmds_path_config), "test_post_command", [])

    try:
        ssh = paramiko_establish_connection(base_url, 'user', command["host"], command["port"], dict())
    except ssh_exception.NoValidConnectionsError as err:
        assert True
    except ssh_exception.SSHException as err:
        assert True
    else:
        assert False


def test_create_request_param_to_config(ssh_server, mock_post_request, base_url, cmds_path_config, test_command):
    """ Check that the function return the correct list of dictionaries """
    dictionary={
        "ssh_port": ssh_server.port,
        "resolution": "1440x900",
        "ppn": "2",
        "mem": "4",
    }

    output = create_request_param_to_config(dictionary) 

    assert isinstance(output, list)
    assert isinstance(output[0], dict)
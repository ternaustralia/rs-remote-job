import pytest
from pathlib import Path
from resource_server.utils.common import paramiko_establish_connection
from resource_server.utils.cmd import execute_command, get_command, get_parameters, _convert


def test_execute_command(ssh_server, mock_post_request, cmds_path_config, test_command, base_url):
    """ Test if is possible to run commands in the remote host """

    command = get_command(test_command, dict(), cmds_path_config )
    command["port"] = ssh_server.port

    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"], dict())
    response = execute_command(ssh, command, "GET")

    # Check that command is received is the ssh server
    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_execute_command_post(ssh_server, mock_post_request, cmds_path_config, base_url):
    """ Test if is possible to run commands in the remote host """

    command = get_command("test_post_command", dict(), cmds_path_config )
    command["port"] = ssh_server.port

    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"], dict())
    response = execute_command(ssh, command, "POST")

    # Check that command is received is the ssh server
    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_get_command(cmds_path_config):
    """ Get the command with the specified parameters """
    p1 = {
        'jobmemory': 10,
        'jobcpu': 3
    }
    commanditem = get_command('command1', p1, cmds_path_config)

    # Check that command are set with the associated parameters
    assert commanditem['exec']['command'] == f"command1 {p1['jobmemory']} {p1['jobcpu']}"
    assert commanditem['host'] == '127.0.0.1'  # match to the parameter 'login' in config file


def test_get_parameters(command_test_item):
    """ Test that the parameter values are set as in parameters specified"""
    p1 = {
        'jobmemory': 10,
        'jobcpu': 3
    }
    gparams = [
        {"name": "loginHost", "type": "string", "default": "login-node-ip"},
        {"name": "loginPort", "type": "int", "default": 4000}
    ]
    params = get_parameters('command1', p1, command_test_item, gparams)

    # Check for pass-in values are set in parameters
    expected_params = {'loginHost': "login-node-ip", "loginPort": 4000}
    expected_params.update(p1)
    assert params == expected_params


def test_get_parameters_default(command_test_item):
    # Test default parameter value
    params = get_parameters('command1', {'jobcpu': 2}, command_test_item, gparams=[])

    # Check that the parameter jobmemory has default value of 4
    expected_params = {'jobmemory': 4, 'jobcpu': 2}
    assert params == expected_params


def test_get_parameters_missing_param(command_test_item):
    # Check that exception is raised for missing parameter
    with pytest.raises(Exception) as e1:
        params = get_parameters('command1', {}, command_test_item, gparams=[])
        assert e1.value.args[0] == "Missing parameter 'jobcpu' for command command1"


def test_convert():
    # Test _convert converts type properly
    vars = [
        ('string', 'string-value', 'string-value'),
        ('int', 100, 100),
        ('int', '101', 101),
        ('int', 100.9, 100),
        ('float', 1.6, 1.6),
        ('float', '1.6', 1.6),
        ('double', 1.766, 1.766),
        ('double', '1.766', 1.766),
        ('bool', 1, True),
        ('bool', 'true', True),
        ('bool', 'True', True),
        ('bool', True, True),
        ('bool', 0, False),
        ('bool', 'false', False),
        ('bool', 'False', False),
        ('bool', False, False)
    ]

    # Check that the converted value is as expected
    for otype, value, expected in vars:
        assert _convert(value, otype) == expected
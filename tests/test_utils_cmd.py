import pytest
from pathlib import Path
from resource_server.utils.common import paramiko_establish_connection
from resource_server.utils.cmd import execute_command, get_command, get_parameters, _convert


def test_execute_command(ssh_server, mock_post_request, command_test_config, test_command, base_url):
    """ Test if is possible to run commands in the remote host """

    command = get_command(test_command, dict(), command_test_config)

    ssh = paramiko_establish_connection(base_url, "user", "localhost", ssh_server.port)
    response = execute_command(ssh, command, "GET")

    # Check that command is received is the ssh server
    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_execute_command_post(ssh_server, mock_post_request, command_test_config, base_url):
    """ Test if is possible to run commands in the remote host """

    command = get_command("test_post_command", dict(), command_test_config)

    ssh = paramiko_establish_connection(base_url, "user", "localhost", ssh_server.port)
    response = execute_command(ssh, command, "POST")

    # Check that command is received is the ssh server
    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_get_command(command_test_config):
    """ Get the command with the specified parameters """
    p1 = {
        'jobmemory': 10,
        'jobcpu': 3
    }
    commanditem = get_command('command1', p1, command_test_config)

    # Check that command are set with the associated parameters
    assert commanditem['exec']['command'] == f"command1 {p1['jobmemory']} {p1['jobcpu']}"
    assert commanditem['connection'] == 'ssh'


def test_get_parameters(command_test_item):
    """ Test that the parameter values are set as in parameters specified"""
    p1 = {
        'jobmemory': 10,
        'jobcpu': 3
    }
    params = get_parameters('command1', p1, command_test_item)

    # Check for pass-in values are set in parameters
    expected_params = p1
    assert params == expected_params


def test_get_parameters_default(command_test_item):
    # Test default parameter value
    params = get_parameters('command1', {'jobcpu': 2}, command_test_item)

    # Check that the parameter jobmemory has default value of 4
    expected_params = {'jobmemory': 4, 'jobcpu': 2}
    assert params == expected_params


def test_get_parameters_missing_param(command_test_item):
    # Check that exception is raised for missing parameter
    with pytest.raises(Exception) as e1:
        params = get_parameters('command1', {}, command_test_item)
        assert e1.value.args[0] == "Missing parameter 'jobcpu' for command command1"


def test_convert():
    # Test _convert converts simple types properly
    vars = [
        ('string', 'string-value', 'string-value'),
        ('integer', 100, 100),
        ('integer', '101', 101),
        ('integer', 100.9, 100),
        ('number', 1.766, 1.766),
        ('number', '1.766', 1.766),
        ('boolean', 1, True),
        ('boolean', 'true', True),
        ('boolean', 'True', True),
        ('boolean', True, True),
        ('boolean', 0, False),
        ('boolean', 'false', False),
        ('boolean', 'False', False),
        ('boolean', False, False)
    ]

    # Check that the converted value is as expected
    for otype, value, expected in vars:
        assert _convert(value, otype) == expected
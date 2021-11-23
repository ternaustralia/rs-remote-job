from resource_server.utils.common import paramiko_establish_connection, validate_schema
from resource_server.utils.cmd import execute_command, load_template_values, load_template_parameters


def test_execute_command(monkeypatch, ssh_server, mock_post_request, cmds_path_config, test_command, base_url):
    """ Check if is possible to run commands in the remote host """

    command = load_template_values(validate_schema(cmds_path_config), test_command)
    monkeypatch.setitem(command, "port", ssh_server.port)

    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"])
    response = execute_command(ssh, command, "GET")

    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_execute_command_post(monkeypatch, ssh_server, mock_post_request, cmds_path_config, base_url):
    """ Check if is possible to run commands in the remote host """

    command = load_template_values(validate_schema(cmds_path_config), "test_post_command")
    monkeypatch.setitem(command, "port", ssh_server.port)

    ssh = paramiko_establish_connection(base_url, "user", command["host"], command["port"])
    response = execute_command(ssh, command, "POST")

    assert isinstance(response, dict)
    assert response['code'] == 200
    assert ssh_server.commands[0] == command['exec']['command']


def test_load_template_values(cmds_path_config, test_command):
    """ Check if the shcema validator is correct and loading the parameters """

    command = load_template_values(validate_schema(cmds_path_config), test_command)
    assert "ls -la ~/ | grep vim" == command["exec"]["command"]


def test_load_template_parameters():
    """ Check if the function is able to create the correct parameters structure """

    parameters = [
        {"name": "login", "type": "string", "default": "login"},
        {"name": "exec", "type": "string", "default": "exec"},
        {"name": "local", "type": "string", "default": "local"},
        {"name": "squeue", "type": "string", "default": "/usr/bin/squeue"},
        {"name": "sacctmgr", "type": "string", "default": "/usr/bin/sacctmgr"},
        {"name": "clearpass", "type": "string", "default": "~/.vnc/clearpass"},
        {"name": "scontrol", "type": "string", "default": "/usr/bin/scontrol"},
        {"name": "scancel", "type": "string", "default": "/usr/bin/scancel"},
        {"name": "coesra-containers", "type": "string", "default": "/nfs/home/public_share_data/installers/coesra-containers"}
    ]

    output = {
        "login":             "login",
        "exec":              "exec",
        "local":             "local",
        "squeue":            "/usr/bin/squeue",
        "sacctmgr":          "/usr/bin/sacctmgr",
        "clearpass":         "~/.vnc/clearpass",
        "scontrol":          "/usr/bin/scontrol",
        "scancel":           "/usr/bin/scancel",
        "coesra-containers": "/nfs/home/public_share_data/installers/coesra-containers"
    }

    response = load_template_parameters(parameters)
    assert response == output

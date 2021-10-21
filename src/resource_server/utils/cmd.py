import re
from paramiko import SSHClient

from resource_server.utils.commond import read_json_file


def execute_command(ssh: SSHClient, endpoint: str) -> tuple: 
    """ Run the specific command and then check for the result """

    commands = read_json_file().get('Commands')
    cmd = commands.get(endpoint)

    if not cmd:
        return {
            'code': 400,
            'message': 'endpoint not valid, please check your request.'
        }

    stdin, stdout, stderr = ssh.exec_command(cmd.get('cmd'))
    lines = stdout.readlines()

    if not stderr.channel.exit_status_ready():
        errorgex = commands.get('messageRegexs')
        info = re.search(errorgex['info'], " ".join(lines), re.IGNORECASE)
        warn = re.search(errorgex['warn'], " ".join(lines), re.IGNORECASE)
        error = re.search(errorgex['error'], " ".join(lines), re.IGNORECASE)

        return (info, warn, error,)

    if not cmd.get('regex'):
        return tuple(lines)

    result = re.search(cmd.get('regex'), " ".join(lines), re.IGNORECASE)
    return result.groups() if result else () 


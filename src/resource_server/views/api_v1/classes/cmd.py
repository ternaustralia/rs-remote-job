import re

from resource_server.utils.commond import paramiko_stablish_connection, read_json_file


class CMD:
    commands = read_json_file().get('Commands')

    def __init__(self):
        self.ssh = paramiko_stablish_connection() 

    def execute(self, endpoint: str) -> tuple: 
        """ Run the specific command and then check for the result """

        cmd = self.commands.get(endpoint)

        if not cmd:
            return {
                'code': 400,
                'message': 'endpoint not valid, please check your request.'
            }

        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))
        lines = stdout.readlines()

        if not stderr.channel.exit_status_ready():
            errorgex = self.commands.get('messageRegexs')
            info = re.search(errorgex['info'], " ".join(lines), re.IGNORECASE)
            warn = re.search(errorgex['warn'], " ".join(lines), re.IGNORECASE)
            error = re.search(errorgex['error'], " ".join(lines), re.IGNORECASE)

            return (info, warn, error,)

        if not cmd.get('regex'):
            return tuple(lines)

        result = re.search(cmd.get('regex'), " ".join(lines), re.IGNORECASE)
        return result.groups() if result else () 

    
from resource_server.utils.commond import paramiko_stablish_connection, read_json_file
class Slurm:
    commands = read_json_file().get('Commands')

    def __init__(self, psskey):
        self.ssh = paramiko_stablish_connection(psskey) 

    def execute(self, endpoint)-> list: 
        cmd = self.commands.get(endpoint)
        if not cmd:
            return {
                'code': 400,
                'message': 'endpoint not valid, please check your request.'
            }

        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.readlines()

    
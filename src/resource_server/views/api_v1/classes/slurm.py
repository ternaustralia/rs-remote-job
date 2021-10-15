from resource_server.utils.commond import paramiko_stablish_connection, read_json_file
class Slurm:
    commands = read_json_file().get('Commands')

    def __init__(self, psskey):
        self.ssh = paramiko_stablish_connection(psskey) 
    
    def user_exists(self):
        """ Check if the user is already created, if no, create the new user """
        cmd = self.commands.get('exists')
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        return stdout.readlines()

    def get_projects(self):
        """ Not Description yet """
        cmd = self.commands.get('getProjects')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def get_usage(self):
        """ Not Description yet """
        cmd = self.commands.get('getUsage')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def stop_process(self):
        """ Not Description yet """
        cmd = self.commands.get('stop')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def start_server(self):
        """ Not Description yet """
        cmd = self.commands.get('startServer')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def list_all(self):
        """ Not Description yet """
        cmd = self.commands.get('listAll')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def exec_host(self):
        """ Not Description yet """
        cmd = self.commands.get('execHost')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()

    def running(self):
        """ Not Description yet """
        cmd = self.commands.get('running')
        stdin, stdout, stderr = self.ssh.exec_command(cmd.get('cmd'))

        return stdout.readlines()
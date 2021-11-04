import unittest

from resource_server.utils.common import paramiko_establish_connection
from resource_server.utils.cmd import execute_command, load_template_values, load_template_parameters

class TestClassesCMD(unittest.TestCase):

    def test_execute_command(self):
        """ Check if is possible to run commands in the remote host """

        ssh = paramiko_establish_connection()
        response = execute_command(ssh, "test_command", "GET")

        self.assertIsInstance(response, dict)
        self.assertEqual(response["code"], 200)

    def test_load_template_values(self):
        """ Check if the shcema validator is correct and loading the parameters """

        command = load_template_values("test_command")

        self.assertEqual("ls -la ~/ | grep vim", command["exec"]["command"])

    def test_load_template_parameters(self):
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
        self.assertDictEqual(response, output)







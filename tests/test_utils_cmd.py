import unittest

from resource_server.utils.commond import paramiko_establish_connection
from resource_server.utils.cmd import execute_command

class TestClassesCMD(unittest.TestCase):

    def test_paramiko_stablish_connection(self):
        """ Check if is possible to run commands in the remote host """

        ssh = paramiko_establish_connection()
        response = execute_command(ssh, "test_command")

        print(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["code"], 200)




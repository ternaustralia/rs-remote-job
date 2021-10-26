import unittest
import paramiko

from resource_server.utils.constants import MASTER_NODE_HOST, MASTER_NODE_PORT, MASTER_NODE_USER 
from resource_server.utils.commond import paramiko_establish_connection, read_json_file

class TestUtilsCommond(unittest.TestCase):

    def test_read_json_file(self):
        """ Test function that reads a json file """
        json_data = read_json_file()

        self.assertIsInstance(json_data, dict)
        self.assertIsNotNone(json_data.get('Commands'))

    def test_paramiko_stablish_connection(self):
        """ Check if paramiko can connect with the host """

        ssh = paramiko_establish_connection()
        self.assertIsInstance(ssh, paramiko.SSHClient)

import unittest
import paramiko

from resource_server.utils.constants import MASTER_NODE_HOST, MASTER_NODE_PORT, MASTER_NODE_USER 
from resource_server.utils.commond import paramiko_stablish_connection, read_json_file

class TestUtilsCommond(unittest.TestCase):

    def test_read_json_file(self):
        """ Test function that reads a json file """
        json_data = read_json_file()

        self.assertIsInstance(json_data, dict)
        self.assertIsNotNone(json_data.get('Commands'))

    def test_paramiko_local_connection(self):
        """ Check if paramiko can connect with local host keys """

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
                hostname=MASTER_NODE_HOST,
                username=MASTER_NODE_USER,
                port=MASTER_NODE_PORT,
            )

        self.assertIsInstance(ssh, paramiko.SSHClient)

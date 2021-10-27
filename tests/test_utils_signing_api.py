import unittest

from resource_server.utils.signing_api import get_keys, check_signature 


class TestSigningApi(unittest.TestCase):

    def test_get_keys(self):
        """ Get new ssh keys and CA """
        keys = get_keys() 

        self.assertIsInstance(keys, dict)
        self.assertIn("cert_key", keys.keys())
        self.assertIn("public_key", keys.keys())
        self.assertIn("private_key", keys.keys())

    def test_check_signature(self):
        """ Verify the signature with the public and certificate """

        keys = get_keys() 
        is_signed = check_signature(keys["public_key"], keys["cert_key"])

        self.assertTrue(is_signed)


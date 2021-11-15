from resource_server.utils.signing_api import get_keys, check_signature

# TODO: should verify that get_keys issues correct _post_request
def test_get_keys(self):
    """ Get new ssh keys and CA """
    keys = get_keys()

    self.assertIsInstance(keys, dict)
    self.assertIn("cert_key", keys.keys())
    self.assertIn("public_key", keys.keys())
    self.assertIn("private_key", keys.keys())


# TODO: should verify that check_signature issues correct _post_request
def test_check_signature(self):
    """ Verify the signature with the public and certificate """

    keys = get_keys()
    is_signed = check_signature(keys["public_key"], keys["cert_key"])

    self.assertTrue(is_signed)

from resource_server.utils.signing_api import get_keys, check_signature

# TODO: should verify that get_keys issues correct _post_request
def test_get_keys(mock_ssh_cert_service):
    """ Get new ssh keys and CA """
    keys = mock_ssh_cert_service.get_keys()

    assert isinstance(keys, dict)
    assert "cert_key" in keys.keys()
    assert "public_key" in keys.keys()
    assert "private_key" in keys.keys()


# TODO: should verify that check_signature issues correct _post_request
def test_check_signature():
    """ Verify the signature with the public and certificate """

    keys = get_keys()
    is_signed = check_signature(keys["public_key"], keys["cert_key"])

    assert True == is_signed

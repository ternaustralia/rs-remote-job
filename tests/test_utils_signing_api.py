from resource_server.utils.signing_api import get_keys, check_signature

# TODO: should verify that get_keys issues correct _post_request
def test_get_keys(mock_post_request, base_url):
    """ Get new ssh keys and CA """
    username = "yong"
    keys = get_keys(base_url, username)

    assert isinstance(keys, dict)
    assert {"cert_key", "public_key", "private_key"} == set(keys.keys())


# TODO: should verify that check_signature issues correct _post_request
def test_check_signature(mock_post_request, get_keys, base_url):
    """ Verify the signature with the public and certificate """
    username = "yong"
    response = check_signature(base_url, username, get_keys["public_key"], get_keys["cert_key"])
    assert (response["code"] == 200) & (response["message"] == "success")

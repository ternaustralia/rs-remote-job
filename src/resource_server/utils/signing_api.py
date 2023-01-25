import requests
from typing import Dict
from flask_tern.auth import oauth


def get_keys(base_url: str, username: str) -> Dict[str, str]:
    """ Call signing key api to generate a new public/private key-pair and cert key using service role """
    return _post_request(f"{base_url}/key/generate", {"username": username})


def check_signature(base_url:str, username: str, public_key: str, cert_key: str) -> Dict[str, str]:
    """ Check if the certificate key is valid using service role"""
    return _post_request(
        f"{base_url}/key/verify",
        {
            "cert_key": cert_key,
            "public_key": public_key,
            "username": username
        }
    )


def _post_request(url: str, params: Dict) -> Dict[str, str]:
    """ post request via service account """
    # create OAuth2 Session
    oidc_md = oauth.oidc.load_server_metadata()
    client = oauth.oidc._get_oauth_client(**oidc_md)

    # fetch access token for service account
    client.fetch_token()
    response = client.post(url, json=params)
    response.raise_for_status()
    return response.json()
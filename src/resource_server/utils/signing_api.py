import json
import requests
from typing import Dict


def get_keys(base_url: str, headers: Dict) -> Dict[str, str]:
    """ Call signing key api and generate a new public, private and cert keys """
    return _post_request(f"{base_url}/key/generate", dict(), headers=headers)


def check_signature(base_url, public_key: str, cert_key: str, headers: Dict) -> Dict[str, str]:
    """ Check if the certificate key is valid """
    return _post_request(
        f"{base_url}/key/verify",
        {
            "cert_key": cert_key,
            "public_key": public_key
        },
        headers=headers
    )


def _get_request(url: str, headers: Dict) -> str:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Check that the request is valid
    if not response:
        raise Exception("Check your credentials or make sure the endpoint is working.")
    return response.text


def _post_request(url: str, params: Dict, headers: Dict) -> Dict[str, str]:
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()


def _del_request(url: str) -> str:
    response = requests.delete(url)
    response.raise_for_status()
    return response.text

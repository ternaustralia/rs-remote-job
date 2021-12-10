import json
import requests
from typing import Dict


def get_keys(base_url: str, headers: Dict) -> Dict[str, str]:
    """ Call signing key api and generate a new public, private and cert keys """
    # Prepare url
    url = f"{base_url}/key/generate"
    # Prepare query
    params = {}

    return _post_request(url, params, headers)

def check_signature(base_url, public_key: str, cert_key: str, header: Dict) -> Dict[str, str]:
    """ Check if the certificate key is valid """
    # Prepare url
    url = f"{base_url}/key/verify"
    # Prepare query
    params = {
        "cert_key": cert_key,
        "public_key": public_key
    }

    return _post_request(url, params, headers)

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

    # Check that the request is valid
    if not response:
        raise Exception(response.text)

    # Decode response in json
    response = json.loads(response.text)

    return response

def _del_request(url: str) -> str:
    response = requests.delete(url)
    response.raise_for_status()

    # Check that the request is valid
    if not response:
        raise Exception(response.text)

    return response.text

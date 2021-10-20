from typing import Dict
import requests
import json

from resource_server.utils.constants import BASE_URL 


class SigningKey:

    def get_keys(self):
        """ Call signing key api and generate a new public, private and cert keys """
        # Prepare url
        url = f'{BASE_URL}/token'
        # Prepare query
        params = {}

        return self._post_request(url, params)

    def check_signature(self, public_key: str, cert_key: str):
        """ Check if the certificate key is valid """
        # Prepare url
        url = f'{BASE_URL}/token/signing'
        # Prepare query
        params = { 
            'cert_key': cert_key, 
            'public_key': public_key
        }

        return self._post_request(url, params)

    def _get_request(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()

        # Check that the request is valid
        if not response:
            raise Exception("Check your credentials or make sure the endpoint is working.")

        return response.text

    def _post_request(self, url: str, params: Dict) -> Dict[str, str]:
        response = requests.post(url, json=params)
        response.raise_for_status()

        # Check that the request is valid
        if not response:
            raise Exception(response.text)

        # Decode response in json
        response = json.loads(response.text)

        return response

    def _del_request(self, url: str) -> str:
        response = requests.delete(url)
        response.raise_for_status()

        # Check that the request is valid
        if not response:
            raise Exception(response.text)

        return response.text

import os
import pytest
import mock_ssh_server
import requests

from pathlib import Path
from flask_tern.testing.fixtures import basic_auth as base_auth  # noqa
from flask_tern.testing.fixtures import cache_spec, monkeypatch_session  # noqa
from resource_server import create_app


@pytest.fixture
def cmds_path_config():
    """Return path to cmds.json config file."""
    return str(Path(__file__).with_name("cmds.json"))


@pytest.fixture
def test_command():
    """Return string with the command to run as a test"""
    return "test_command"


@pytest.fixture
def base_url():
    """Return url to use as a host that runs the key-signing"""
    return "http://127.0.0.1/api/v1.0"


@pytest.fixture
def app(cmds_path_config, base_url):
    app = create_app(
        {
            "TESTING": True,
            "OIDC_DISCOVERY_URL": "https://auth.example.com/.well-known/openid-configuration",
            "OIDC_CLIENT_ID": "oidc-test",
            "SSH_PRINCIPAL_CLAIM": "coesra_uname",
            "CMD_PATH_FILE": cmds_path_config,
            "SSH_KEYSIGN_BASE_URL": base_url,
        }
    )
    yield app


@pytest.fixture
def basic_auth(base_auth):  # noqa
    for key, user in base_auth.items():
        base_auth[key].claims["coesra_uname"] = user.name
    return base_auth


@pytest.fixture
def client(app, basic_auth):  # noqa
    return app.test_client()


@pytest.fixture
def ssh_server():
    with mock_ssh_server.Server() as server:
        yield server


@pytest.fixture
def get_keys():
    return {
        "private_key": Path(__file__).with_name("test_user.key").read_text(),
        "public_key": Path(__file__).with_name("test_user.key.pub").read_text(),
        "cert_key": Path(__file__).with_name("test_user.key-cert.pub").read_text(),
    }


@pytest.fixture
def mock_post_request(monkeypatch, get_keys):
    def _post_request(url, json):
        base_name = os.path.basename(url)

        if base_name == 'generate':
            return get_keys
        elif base_name == 'verify':
            return {"message": "success", "code": 200}
        elif base_name == 'sign':
            return {
                "public_key": get_keys["public_key"],
                "cert_key": get_keys["cert_key"]
            }
        else:
            return {"message": "Error", "code": 404}

    monkeypatch.setattr("resource_server.utils.signing_api._post_request", _post_request)



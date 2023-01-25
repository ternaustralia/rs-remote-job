import os
import pytest
import yaml
import mock_ssh_server
import requests

from pathlib import Path
from flask_tern.testing.fixtures import basic_auth as base_auth  # noqa
from flask_tern.testing.fixtures import cache_spec, monkeypatch_session  # noqa
from resource_server import create_app


@pytest.fixture
def cmds_path_config():
    """Return path to cmds.yaml config file."""
    return str(Path(__file__).with_name("cmds.yaml"))


@pytest.fixture
def command_test_config(cmds_path_config):
    """Return configuration settings of config yaml file'"""
    with open(cmds_path_config) as f1:
        config = yaml.safe_load(f1)
    return config

@pytest.fixture
def command_test_item(command_test_config):
    """Return a command item with name 'command1'"""
    for cmditem in command_test_config['endpoints']:
        if cmditem['name'] == 'command1':
            return cmditem


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


@pytest.fixture(scope="session")
def ssh_server(request):
    with mock_ssh_server.Server(port=6060) as server:
        yield server


@pytest.fixture(scope="session")
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

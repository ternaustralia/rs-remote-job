from pathlib import Path
import pytest
from flask_tern.testing.fixtures import basic_auth as base_auth  # noqa
from flask_tern.testing.fixtures import cache_spec, monkeypatch_session  # noqa
from ssh_cert_service import create_app

import mock_ssh_server

@pytest.fixture
def cmds_config():
    """Return path to cmds.json config file."""
    return str(Path(__file__).with_name("cmds.json"))

@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "OIDC_DISCOVERY_URL": "https://auth.example.com/.well-known/openid-configuration",
            "OIDC_CLIENT_ID": "oidc-test",
        }
    )
    yield app


@pytest.fixture
def basic_auth(base_auth):  # noqa
    for key, value in base_auth.items():
        base_auth[key].claims["coesra_uname"] = value["name"]
    return base_auth


@pytest.fixture
def client(app, basic_auth):  # noqa
    return app.test_client()


@pytest.fixture
def ssh_server():
    with mock_ssh_server.Server() as server:
        yield server

@pytest.fixture
def mock_ssh_cert_service(monkeypatch):

    def get_keys():
        return {
            "private_key": Path(__file__).with_name("test_user.key").read_text(),
            "public_key": Path(__file__).with_name("test_user.key.pub").read_text(),
            "cert_key": Path(__file__).with_name("test_user.key-cert.pub").read_text(),
        }

    monkeypatch.setattr("resource_server.utils.common.get_keys", get_keys)

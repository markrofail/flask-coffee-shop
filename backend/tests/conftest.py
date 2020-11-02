from os import getenv

import pytest
import requests
from dotenv import load_dotenv

from src.api import create_app, db_drop_and_create_all
from src.models import Drink

from .factories import DrinkFactory

load_dotenv()


@pytest.fixture
def app():
    app = create_app()
    db_drop_and_create_all()
    return app


@pytest.fixture(scope="module")
def jwt_token():
    auth_domain = getenv("AUTH0_DOMAIN")
    auth_audience = getenv("AUTH0_API_AUDIENCE")
    client_id = getenv("AUTH0_CLIENT_ID")
    client_secret = getenv("AUTH0_CLIENT_SECRET")

    response = requests.post(
        f"{auth_domain}/oauth/token",
        dict(
            client_id=client_id,
            client_secret=client_secret,
            audience=auth_audience,
            grant_type="client_credentials",
        ),
    )

    token = response.json().get("access_token", None)
    return token


@pytest.fixture
def disable_auth(monkeypatch):
    auth_methods = [
        "get_token_auth_header",
        "verify_decode_jwt",
        "check_permissions",
    ]
    for method in auth_methods:
        monkeypatch.setattr(f"src.auth.auth.{method}", lambda *args: None)

# mocking role in connection
def _make_request_as(monkeypatch, permissions):
    mock = dict(permissions=permissions)

    monkeypatch.setattr("src.auth.auth.get_token_auth_header", lambda *args: None)
    monkeypatch.setattr("src.auth.auth.verify_decode_jwt", lambda *args: mock)


@pytest.fixture
def make_request_as_customer(monkeypatch):
    _make_request_as(monkeypatch, [])


@pytest.fixture
def make_request_as_barista(monkeypatch):
    _make_request_as(monkeypatch, ["get:drinks-detail"])


@pytest.fixture
def make_request_as_manager(monkeypatch):
    _make_request_as(
        monkeypatch,
        [
            "post:drinks",
            "patch:drinks",
            "delete:drinks",
            "get:drinks-detail",
        ],
    )

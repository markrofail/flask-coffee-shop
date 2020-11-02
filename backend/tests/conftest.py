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
    def empty_func(_1=None, _2=None):
        pass

    monkeypatch.setattr("src.auth.auth.get_token_auth_header", empty_func)
    monkeypatch.setattr("src.auth.auth.verify_decode_jwt", empty_func)
    monkeypatch.setattr("src.auth.auth.check_permissions", empty_func)

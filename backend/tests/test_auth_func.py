import pytest
from flask import url_for

from src.auth import auth

from .factories import DrinkFactory


# get_token_auth_header tests =============================
def test_get_token_auth_header_without_header(client):
    # make a request
    client.get("/")

    # assert raises error
    with pytest.raises(auth.AuthError):
        auth.get_token_auth_header()


def test_get_token_auth_header_without_bearer(client):
    # make a request
    headers = dict(Authorization="")
    client.get("/", headers=headers)

    # assert raises error
    with pytest.raises(auth.AuthError):
        auth.get_token_auth_header()


def test_get_token_auth_header_wrong_prefix(client):
    # make a request
    headers = dict(Authorization="Token asdAEad")
    client.get("/", headers=headers)

    # assert raises error
    with pytest.raises(auth.AuthError):
        auth.get_token_auth_header()


def test_get_token_auth_header_success(client):
    # make a request
    headers = dict(Authorization="Bearer asdAEad")
    client.get("/", headers=headers)

    # assert correct output
    token = auth.get_token_auth_header()
    assert token == "asdAEad"


# verify_decode_jwt test ==================================
def test_verify_decode_jwt(jwt_token):
    if not jwt_token:
        pytest.skip("unsupported configuration")

    response = auth.verify_decode_jwt(jwt_token)


# check_permissions test ==================================
def test_check_permissions_invalid_payload():
    # empty payload
    payload = dict()

    # assert correct output
    with pytest.raises(auth.AuthError):
        auth.check_permissions("post:drinks", payload)


def test_check_permissions_empty_permissions():
    # empty permissions
    payload = dict(permissions=[])

    # assert correct output
    with pytest.raises(auth.AuthError):
        auth.check_permissions("post:drinks", payload)


def test_check_permissions_incorrect_permissions():
    # incorrect permissions
    payload = dict(permissions=["patch:drinks"])

    # assert correct output
    with pytest.raises(auth.AuthError):
        auth.check_permissions("post:drinks", payload)


def test_check_permissions_correct():
    # correct permissions
    payload = dict(permissions=["post:drinks"])

    response = auth.check_permissions("post:drinks", payload)
    assert response == True

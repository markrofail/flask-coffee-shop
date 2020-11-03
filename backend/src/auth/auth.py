import base64
import json
from functools import wraps
from os import getenv
from urllib.request import urlopen

import requests
from dotenv import load_dotenv
from flask import _request_ctx_stack, abort, request
from jose import jwt

load_dotenv()

# AuthError Exception
class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    """
    get_token_auth_header()
        it should attempt to get the header from the request
            it should raise an AuthError if no header is present
        it should attempt to split bearer and the token
            it should raise an AuthError if the header is malformed
        return the token part of the header
    """

    if "Authorization" not in request.headers:
        raise AuthError("header not found", 401)
    token = request.headers.get("Authorization")

    prefix = "Bearer "
    if not token.startswith(prefix):
        raise AuthError("header malformed", 401)

    token = token[len(prefix) :]
    return token


def check_permissions(permission, payload):
    """
    check_permissions(permission, payload)
        @INPUTS
            permission: string permission (i.e. 'post:drink')
            payload: decoded jwt payload

        it should raise an AuthError if permissions are not included in the payload
        it should raise an AuthError if the requested permission string is not in the payload permissions array
        return true otherwise
    """

    if "permissions" not in payload:
        raise AuthError("header malformed", 401)

    if permission not in payload["permissions"]:
        raise AuthError("insufficient permissions", 403)

    return True


def verify_decode_jwt(token):
    """
    verify_decode_jwt(token)
        @INPUTS
            token: a json web token (string)

        it should be an Auth0 token with key id (kid)
        it should verify the token using Auth0 /.well-known/jwks.json
        it should decode the payload from the token
        it should validate the claims
        return the decoded payload
    """
    auth_domain = getenv("AUTH0_DOMAIN")
    auth_alg = getenv("AUTH0_JWT_ALGORITHM")
    auth_audience = getenv("AUTH0_API_AUDIENCE")

    # ensure token matches pattern header.payload.signatured
    jwt_parts = token.split(".")
    if len(jwt_parts) != 3:
        raise AuthError("header malformed", 401)

    header, payload, signature = jwt_parts
    header = base64.b64decode(header)
    header = json.loads(header)

    # ensure kid is in the header
    if "kid" not in header:
        raise AuthError("Auth token not authentic", 401)
    kid = header["kid"]

    # get jwt key store
    try:
        jwks = requests.get(f"{auth_domain}/.well-known/jwks.json")
        jwks = jwks.json().get("keys", None)
        assert jwks
    except Exception:
        raise AuthError("could not connect to the sever", 500)

    # match rsa public key to kid
    matching_rsa = None
    for key in jwks:
        if key.get("kid", "") == kid:
            matching_rsa = key
    if not matching_rsa:
        raise AuthError("token not authentic", 401)

    # decode jwt
    try:
        payload = jwt.decode(
            token,
            matching_rsa,
            algorithms=[auth_alg],
            audience=auth_audience,
            issuer=f"{auth_domain}/",
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("expired token", 401)
    except jwt.JWTClaimsError:
        raise AuthError("invalid claims", 401)
    except Exception:
        raise AuthError("header malformed", 401)

    return payload


def requires_auth(permission=""):
    """
    @requires_auth(permission) decorator
        @INPUTS
            permission: string permission (i.e. 'post:drink')

        it should use the get_token_auth_header method to get the token
        it should use the verify_decode_jwt method to decode the jwt
        it should use the check_permissions method validate claims and check the requested permission
        return the decorator which passes the decoded payload to the decorated method
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as exec:
                abort(exec.status_code)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator

import json
import os
from functools import partial

from flask import Blueprint, Flask, abort, jsonify, request
from flask_cors import CORS
from sqlalchemy import exc

from src.auth.auth import AuthError, requires_auth
from src.models import db_drop_and_create_all, setup_db
from src.serializers import (drink_schema, drinks_brief_schema, drinks_schema,
                             ma)
from src.services import (add_drink, delete_drink, get_all_drinks, get_drink,
                          update_drink)

drink_api = Blueprint("drinks", "")


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    ma.init_app(app)

    register_errorhandlers(app)
    app.register_blueprint(drink_api)
    return app


"""
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UN-COMMENTED ON FIRST RUN
"""
# db_drop_and_create_all()


@drink_api.route("/drinks", methods=["GET"])
def drinks_list():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    queryset = get_all_drinks()
    return jsonify(drinks=drinks_brief_schema.dump(queryset), success=True)


@drink_api.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def drinks_list_detail():
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    queryset = get_all_drinks()
    return jsonify(drinks=drinks_schema.dump(queryset), success=True)


@drink_api.route("/drinks/<int:drink_id>", methods=["GET"])
@requires_auth("get:drinks-detail")
def drinks_detail(drink_id):
    """
    GET /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
    returns status code 200 and json {"success": True, "drink": drink}
    """
    queryset = get_drink(drink_id)
    if not queryset:
        abort(404)

    return jsonify(drink=drink_schema.dump(queryset), success=True)


@drink_api.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def drinks_create():
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    """
    drink_json = request.get_json()
    errors = drink_schema.validate(drink_json)
    if errors:
        abort(422)

    drink_json = drink_schema.load(drink_json)
    drink_id = add_drink(drink_json)

    queryset = get_drink(drink_id)
    return jsonify(drinks=drinks_schema.dump([queryset]), success=True)


@drink_api.route("/drinks/<drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def drinks_update(drink_id):
    """
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    queryset = get_drink(drink_id)
    if not queryset:
        abort(404)

    drink_json = request.get_json()
    errors = drink_schema.validate(drink_json, partial=True)
    if errors:
        abort(422)

    drink_json = drink_schema.load(drink_json, partial=True)
    updated_queryset = update_drink(queryset, drink_json)

    return jsonify(drinks=drinks_schema.dump([updated_queryset]), success=True)


@drink_api.route("/drinks/<int:drink_id>/", methods=["DELETE"])
@requires_auth("delete:drinks")
def drinks_delete(drink_id):
    """
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    queryset = get_drink(drink_id)
    if not queryset:
        abort(404)

    delete_drink(queryset)
    return jsonify(delete=drink_id, success=True)


# Error Handling
def register_errorhandlers(app):
    def return_error_message(status_code, error_message, _):
        return (
            jsonify(success=False, error=status_code, message=error_message),
            status_code,
        )

    for status_code, error_message in [
        (400, "bad request"),
        (401, "unauthorized"),
        (404, "resource not found"),
        (403, "insufficient permissions"),
        (422, "unprocessable"),
        (500, "server fault"),
    ]:
        handler_func = partial(return_error_message, status_code, error_message)
        app.register_error_handler(status_code, handler_func)

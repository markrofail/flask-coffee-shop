import pytest
from flask import url_for

from .factories import DrinkFactory


# GET /drinks tests =======================================
def test_get_all(client):
    """GET /drinks: returns correct data"""

    # insert some drinks in the database
    map(lambda drink: drink.insert(), DrinkFactory.create_batch(5))

    # make request at GET /drinks
    res = client.get(url_for("drinks.drinks_list"))

    # assert correct data return
    assert res.json.get("success", None) == True
    assert len(res.json.get("drinks", [])) == 5


def test_get_all_is_short(client):
    """GET /drinks: returns recipe in short format"""

    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    # make request at GET /drinks
    res = client.get(url_for("drinks.drinks_list"))

    # assert correct data return
    assert len(res.json.get("drinks", [])) == 1
    drink_json = res.json["drinks"][0]

    recipe_json = drink_json.get("recipe", {})
    assert list(recipe_json.keys()) == ["color", "parts"]


# GET /drinks-detail tests ================================
@pytest.mark.usefixtures("disable_auth")
def test_get_all_detail(client):
    """GET /drinks-details: returns correct data"""

    # insert some drinks in the database
    map(lambda drink: drink.insert(), DrinkFactory.create_batch(5))

    # make request at GET /drinks-detail
    res = client.get(url_for("drinks.drinks_list_detail"))

    # assert correct data return
    assert res.json.get("success", None) == True
    assert len(res.json.get("drinks", [])) == 5


@pytest.mark.usefixtures("disable_auth")
def test_get_all_detail_is_detail(client):
    """GET /drinks-details: returns recipe in long format"""

    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    # make request at GET /drinks-detail
    res = client.get(url_for("drinks.drinks_list_detail"))

    # assert correct data return
    assert len(res.json.get("drinks", [])) == 1
    drink_json = res.json["drinks"][0]

    recipe_json = drink_json.get("recipe", {})
    assert list(recipe_json.keys()) == ["color", "name", "parts"]


# GET /drinks/<id> tests ================================
@pytest.mark.usefixtures("disable_auth")
def test_get_one_detail(client):
    """GET /drinks/<id>: returns correct data"""

    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    # make request at GET /drinks/1
    res = client.get(url_for("drinks.drinks_detail", drink_id=drink.id))

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("drink", None) is not None


@pytest.mark.usefixtures("disable_auth")
def test_get_one_detail_correct_404(client):
    """GET /drinks/<id>: returns 404 on not found"""

    # make request at GET /drinks/1
    res = client.get(url_for("drinks.drinks_detail", drink_id=1))

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 404


# POST /drinks tests ======================================
@pytest.mark.usefixtures("disable_auth")
def test_post_new_drink(client):
    """POST /drinks: successful"""

    payload = dict(
        title="Test Drink", recipe=dict(name="Test Recipe", color="#ffffff", parts="1")
    )

    # make request at POST /drinks
    res = client.post(url_for("drinks.drinks_create"), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("drinks", None) is not None

    drink_json = res.json["drinks"][0]
    assert drink_json["title"] == payload["title"]
    assert drink_json["recipe"]["name"] == payload["recipe"]["name"]
    assert drink_json["recipe"]["color"] == payload["recipe"]["color"]
    assert drink_json["recipe"]["parts"] == payload["recipe"]["parts"]


@pytest.mark.usefixtures("disable_auth")
def test_post_new_drink_missing_recipe(client):
    """POST /drinks: returns 422 on missing recipe"""

    payload = dict(
        title="Test Drink",
    )

    # make request at POST /drinks
    res = client.post(url_for("drinks.drinks_create"), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 422


@pytest.mark.usefixtures("disable_auth")
def test_post_new_drink_missing_title(client):
    """POST /drinks: returns 422 on missing title"""

    payload = dict(recipe=[dict(name="Test Recipe", color="#ffffff", parts="1")])

    # make request at POST /drinks
    res = client.post(url_for("drinks.drinks_create"), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 422


# PATCH /drinks tests =====================================
@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_success(client):
    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    payload = dict(
        title="Test Drink",
        recipe=[dict(name="Test Recipe", color="#ffffff", parts="1")],
    )

    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=drink.id), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("drinks", None) is not None

    drink_json = res.json["drinks"][0]
    assert drink_json["title"] == payload["title"]
    assert drink_json["recipe"][0]["name"] == payload["recipe"][0]["name"]
    assert drink_json["recipe"][0]["color"] == payload["recipe"][0]["color"]
    assert drink_json["recipe"][0]["parts"] == payload["recipe"][0]["parts"]


@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_notfound(client):
    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 404


@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_partial_title(client):
    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    payload = dict(
        title="Test Drink",
    )

    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=drink.id), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("drinks", None) is not None

    drink_json = res.json["drinks"][0]
    assert drink_json["title"] == payload["title"]


@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_partial_recipe(client):
    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    payload = dict(recipe=dict(name="Test Recipe", color="#ffffff", parts="1"))

    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=drink.id), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("drinks", None) is not None

    drink_json = res.json["drinks"][0]
    assert drink_json["recipe"]["name"] == payload["recipe"]["name"]
    assert drink_json["recipe"]["color"] == payload["recipe"]["color"]
    assert drink_json["recipe"]["parts"] == payload["recipe"]["parts"]


@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_int_name(client):
    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    payload = dict(name=1)

    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=drink.id), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 422


@pytest.mark.usefixtures("disable_auth")
def test_patch_drink_invalid_recipe(client):
    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()

    payload = [dict(recipe=dict(name="Test Recipe", parts="1"))]

    # make request at PATCH /drinks/1
    res = client.patch(url_for("drinks.drinks_update", drink_id=drink.id), json=payload)

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 422


# DELETE /drinks tests =====================================
@pytest.mark.usefixtures("disable_auth")
def test_delete_drink_success(client):
    """DELETE /drinks/<id>: returns correct data"""

    # insert some drinks in the database
    drink = DrinkFactory.create()
    drink.insert()
    drink_id = drink.id

    # make request at DELETE /drinks/1
    res = client.delete(url_for("drinks.drinks_delete", drink_id=drink_id))

    # assert correct data return
    assert res.json.get("success", None) == True
    assert res.json.get("delete", None) == drink_id


@pytest.mark.usefixtures("disable_auth")
def test_delete_drink_notfound(client):
    """DELETE /drinks/<id>: returns 404 on not found"""

    # make request at DELETE /drinks/1
    res = client.delete(url_for("drinks.drinks_delete", drink_id=1))

    # assert correct data return
    assert res.json.get("success", None) == False
    assert res.json.get("error", None) == 404

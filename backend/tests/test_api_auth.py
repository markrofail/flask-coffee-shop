import pytest
from flask import url_for


# GET /drinks tests =======================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_get_drinks_as_manager(client):
    res = client.get(url_for("drinks.drinks_list"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_barista")
def test_get_drinks_as_barista(client):
    res = client.get(url_for("drinks.drinks_list"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_customer")
def test_get_drinks_as_customer(client):
    res = client.get(url_for("drinks.drinks_list"))
    assert res.status_code == 200


# GET /drinks-detail tests ================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_get_drinks_detail_as_manager(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_barista")
def test_get_drinks_detail_as_barista(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_customer")
def test_get_drinks_detail_as_customer(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 403


# GET /drinks/<id> tests ================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_get_drinks_one_detail_as_manager(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_barista")
def test_get_drinks_one_detail_as_barista(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 200


@pytest.mark.usefixtures("make_request_as_customer")
def test_get_drinks_one_detail_as_customer(client):
    res = client.get(url_for("drinks.drinks_list_detail"))
    assert res.status_code == 403


# POST /drinks tests ======================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_post_drink_as_manager(client):
    res = client.post(url_for("drinks.drinks_create"), json=dict())
    # allowed but wrong request
    assert res.status_code == 422


@pytest.mark.usefixtures("make_request_as_barista")
def test_post_drink_as_barista(client):
    res = client.post(url_for("drinks.drinks_create"), json=dict())
    assert res.status_code == 403


@pytest.mark.usefixtures("make_request_as_customer")
def test_post_drink_as_customer(client):
    res = client.post(url_for("drinks.drinks_create"), json=dict())
    assert res.status_code == 403


# PATCH /drinks tests =====================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_patch_drink_as_manager(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    # allowed but wrong request
    assert res.status_code == 404


@pytest.mark.usefixtures("make_request_as_barista")
def test_patch_drink_as_barista(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    assert res.status_code == 403


@pytest.mark.usefixtures("make_request_as_customer")
def test_patch_drink_as_customer(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    assert res.status_code == 403


# DELETE /drinks tests =====================================
@pytest.mark.usefixtures("make_request_as_manager")
def test_delete_drink_as_manager(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    # allowed but wrong request
    assert res.status_code == 404


@pytest.mark.usefixtures("make_request_as_barista")
def test_delete_drink_as_barista(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    assert res.status_code == 403


@pytest.mark.usefixtures("make_request_as_customer")
def test_delete_drink_as_customer(client):
    res = client.patch(url_for("drinks.drinks_update", drink_id=1), json=dict())
    assert res.status_code == 403

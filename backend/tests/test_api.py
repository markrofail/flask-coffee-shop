import pytest
from flask import url_for

from .factories import DrinkFactory


def test_get_all(client):
    # insert some drinks in the database
    map(lambda drink: drink.insert(), DrinkFactory.create_batch(5))

    # mock request at GET /drinks
    res = client.get(url_for('drinks.drinks_list'))

    # assert correct data return
    assert res.json.get('success', None) == True
    assert len(res.json.get('drinks', [])) == 5

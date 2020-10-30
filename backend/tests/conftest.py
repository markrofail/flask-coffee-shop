import pytest
from src.api import create_app, db_drop_and_create_all
from src.models import Drink
from .factories import DrinkFactory

@pytest.fixture
def app():
    app = create_app()
    db_drop_and_create_all()
    return app

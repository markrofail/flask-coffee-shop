import json

import factory
from factory.faker import faker

from src.models import Drink, db


class DrinkFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Drink
        sqlalchemy_session = db.session

    title = factory.Faker("numerify", text="Drink ####")

    @factory.lazy_attribute
    def recipe(self):
        gen = faker.Faker()

        recipe_dict = dict(
            name=gen.lexify(),
            color=gen.color(),
            parts=gen.random_digit(),
        )

        return json.dumps(recipe_dict)

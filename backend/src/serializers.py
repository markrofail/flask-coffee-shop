import json

from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE, ValidationError, fields, validates

from .models import Drink

ma = Marshmallow()


class DrinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Drink
        include_fk = True
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    recipe = fields.Method("get_recipe", deserialize="store_recipe", required=True)

    def get_recipe(self, obj):
        full_recipe = json.loads(obj.recipe)
        return full_recipe

    def store_recipe(self, value):
        return json.dumps(value)

    @validates("recipe")
    def validate_recipe(self, value):
        def validate_ingredient(ingredient):
            incoming_fields = sorted(ingredient.keys())
            required_fields = ["color", "name", "parts"]
            if required_fields != incoming_fields:
                raise ValidationError("invalid recipe")

        try:
            incoming_recipe = json.loads(value)
        except json.JSONDecodeError as exec:
            raise ValidationError("invalid recipe")

        map(validate_ingredient, incoming_recipe)


drink_schema = DrinkSchema()
drinks_schema = DrinkSchema(many=True)


class DrinkBriefSchema(DrinkSchema):
    def get_recipe(self, obj):
        full_recipe = json.loads(obj.recipe)
        return [
            dict(color=ingredient.get("color", ""), parts=ingredient.get("parts", ""))
            for ingredient in full_recipe
        ]


drink_brief_schema = DrinkBriefSchema()
drinks_brief_schema = DrinkBriefSchema(many=True)

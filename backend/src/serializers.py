import json

from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, fields, validates

from .models import Drink

ma = Marshmallow()


class DrinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Drink
        include_fk = True

    title = ma.auto_field(required=True)
    recipe = fields.Method("get_recipe", deserialize="store_recipe", required=True)

    def get_recipe(self, obj):
        full_recipe = json.loads(obj.recipe)
        return full_recipe

    def store_recipe(self, value):
        return json.dumps(value)

    @validates("recipe")
    def validate_recipe(self, value):
        try:
            incoming_recipe = json.loads(value)
            incoming_fields = sorted(incoming_recipe.keys())
        except json.JSONDecodeError as exec:
            raise ValidationError("invalid recipe")

        recipe_fields = ["color", "name", "parts"]
        if recipe_fields != incoming_fields:
            raise ValidationError("invalid recipe")


drink_schema = DrinkSchema()
drinks_schema = DrinkSchema(many=True)


class DrinkBriefSchema(DrinkSchema):
    def get_recipe(self, obj):
        full_recipe = json.loads(obj.recipe)
        return dict(
            color=full_recipe.get("color", ""), parts=full_recipe.get("parts", "")
        )


drink_brief_schema = DrinkBriefSchema()
drinks_brief_schema = DrinkBriefSchema(many=True)

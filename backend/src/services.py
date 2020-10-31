from .models import Drink


def get_all_drinks():
    all_drinks = Drink.query.all()
    return all_drinks


def get_drink(drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    return drink


def add_drink(payload):
    drink = Drink(**payload)
    drink.insert()
    return drink.id


def update_drink(instance, payload):
    instance.update(payload)
    return instance


def delete_drink(instance):
    instance.delete()
    return True

import json
import os
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

project_dir = Path(__name__).parent / "database"
database_filename = "database.db"
database_path = "sqlite:///{}".format(project_dir / database_filename)

db = SQLAlchemy()


def setup_db(app):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """
    db_drop_and_create_all()
        drops the database tables and starts fresh
        can be used to initialize a clean database
        !!NOTE you can change the database_filename variable to have multiple versions of a database
    """
    db.drop_all()
    db.create_all()


class Drink(db.Model):
    """
    Drink
    a persistent drink entity, extends the base SQLAlchemy Model
    """

    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)

    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    def insert(self):
        """
        insert()
            inserts a new model into a database
            the model must have a unique name
            the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """
        update()
            updates a new model into a database
            the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.update({title='Black Coffee'})
        """
        db.session.query(Drink).filter(Drink.id == self.id).update(data)
        db.session.commit()

    def __repr__(self):
        return f"<Drink {self.title}>"

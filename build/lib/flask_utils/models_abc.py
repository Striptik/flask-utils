"""
Define an Abstract Base Class (ABC) for models
"""
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from weakref import WeakValueDictionary

db = SQLAlchemy()


class MetaBaseModel(db.Model.__class__):
    """Define a metaclass for the BaseModel
    Implement `__getitem__` for managing aliases"""

    def __init__(cls, *args):
        super().__init__(*args)
        cls.aliases = WeakValueDictionary()

    def __getitem__(cls, key):
        try:
            alias = cls.aliases[key]
        except KeyError:
            alias = aliased(cls)
            cls.aliases[key] = alias
        return alias


class BaseModel:
    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def repr(self):
        return f"{self.__class__.__name__}({json.dumps(self.tojson(), indent=4, sort_keys=True)})"

    def tojson(self):
        return {
            column: value
            if not isinstance(value, datetime)
            else value.strftime("%Y-%m-%d")
            for column, value in self.todict().items()
        }

    def todict(self):
        excl = ("_sa_adapter", "_sa_instance_state")
        return {
            k: v
            for k, v in vars(self).items()
            if not k.startswith("_") and not any(hasattr(v, a) for a in excl)
        }

    def save(self):
        session = db.create_scoped_session()
        try:
            session.add(self)
            session.commit()
            return self
        except Exception:
            session.rollback()
            raise

    def delete(self):
        session = db.create_scoped_session()
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

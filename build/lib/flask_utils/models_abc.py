"""
Define an Abstract Base Class (ABC) for models
"""
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import aliased
from sqlalchemy.orm.collections import CollectionAdapter
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


def get_value(value):
    try:
        class_dict = value.__dict__
        if "_sa_instance_state" in class_dict:
            class_dict.pop("_sa_instance_state", None)
        return class_dict
    except Exception:
        return value if not isinstance(value, datetime) else value.strftime("%d/%m/%Y")


def json_default(value):
    if isinstance(value, datetime):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, CollectionAdapter):
        return []
    else:
        return value.__dict__


class BaseModel:
    """Generalize __init__, __repr__ and to_json
    Based on the models columns"""

    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        """Define a base way to print models
        Columns inside `print_filter` are excluded"""
        return "%s(%s)" % (
            self.__class__.__name__,
            {
                column: value.__dict__
                for column, value in self._to_dict().items()
                if column not in self.print_filter
            },
        )

    def __str__(self):
        object_hash = {
            column: get_value(value)
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        }
        return "%s(%s)" % (
            self.__class__.__name__,
            json.dumps(
                object_hash, default=lambda o: json_default(o), sort_keys=True, indent=4
            ),
        )

    @property
    def json(self):
        """Define a base way to jsonify models
        Columns inside `to_json_filter` are excluded"""
        return {
            column: value
            if not isinstance(value, datetime)
            else value.strftime("%Y-%m-%d")
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        """This would more or less be the same as a `to_json`
        But putting it in a "private" function
        Allows to_json to be overriden without impacting __repr__
        Or the other way around
        And to add filter lists"""
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

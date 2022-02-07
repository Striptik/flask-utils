import json
import datetime


def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


def jsonify(self):
    return json.dumps(self, default=lambda o: json_default(o), sort_keys=True, indent=4)


def jsonify_model(model, keys):
    object_hash = {}
    for key in keys:
        object_hash[key] = getattr(model, key)
    return json.dumps(
        object_hash, default=lambda o: json_default(o), sort_keys=True, indent=4
    )

import json


def jsonify(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def jsonify_model(model, keys):
    object_hash = {}
    for key in keys:
        object_hash[key] = getattr(model, key)
    return json.dumps(
        object_hash, default=lambda o: o.__dict__, sort_keys=True, indent=4
    )

import json
import os

import requests

from flask_utils.logger import log_error, log_exception
from flask_utils.cache import get_cache, set_cache, del_cache


def get_cache_key(name, _id, is_light=False):
    env = os.getenv("ENVIRONMENT", "dev")
    return f"{name.lower()}_{env}_{_id}{'_light' if is_light else ''}"


def get_entity_cache(host, _id: int, path, name, is_light=False):
    try:
        key = get_cache_key(name, _id, is_light)
        cached_entity = get_cache(key)
        if cached_entity:
            return json.loads(cached_entity)
        else:
            entity = get_entity(host=host, _id=_id, path=path, name=name, is_light=is_light)
            if entity is None or entity is False:
                return None
            try:
                set_cache(key, json.dumps(entity))
            finally:
                return entity
    except Exception as e:
        log_error(f"Failed to get {name} in cache", {"_id": _id})
        return get_entity(host=host, _id=_id, path=path, name=name)


def reset_entity_cache(_id: int, name):
    try:
        del_cache(get_cache_key(name, _id, True))
        del_cache(get_cache_key(name, _id, False))
    except Exception as e:
        log_error(f"Failed to reset {name} {_id} in cache", {"_id": _id})


def get_entity(host, _id: int, path, name, is_light=False):
    try:
        query_params = '?isLight=true' if is_light else ''
        response = requests.get(f"{host}/api/{path}/{_id}{query_params}")
        response_json = json.loads(response.content.decode("utf-8"))
        if response.status_code >= 300:
            log_error(
                f"Failed to get {name}", {"response": response_json, "id": _id}
            )
            return None
        return response_json
    except Exception as e:
        log_exception(e, {"id": _id})
        return False


def list_from_ids(host, ids, result_key, path, name):
    try:
        response = requests.get(f"{host}/api/{path}?ids={ids}")
        response_json = response.content.decode("utf-8")
        if response.status_code >= 300:
            log_error(
                f"Failed to get {name}", {"response": response_json, "ids": ids}
            )
            return []
        return json.loads(response_json).get(result_key)
    except Exception as e:
        log_exception(e, {"ids": ids})
        return []


def get_entities(host, entities, id_key, result_key, path, name):
    ids = ",".join(str(getattr(entity, id_key)) for entity in entities)
    return list_from_ids(host, ids, result_key, path, name)

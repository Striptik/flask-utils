import json

import requests

from flask_utils import logger


def get_entity(host, _id: int, path, name):
    try:
        response = requests.get(f"{host}/api/{path}/{_id}")
        response_json = json.loads(response.content.decode("utf-8"))
        if response.status_code >= 300:
            logger.log_error(
                f"Failed to get {name}", {"response": response_json, "id": _id}
            )
            return None
        return response_json
    except Exception as e:
        logger.log_exception(e, {"id": _id})
        return False


def list_from_ids(host, ids, result_key, path, name):
    try:
        response = requests.get(f"{host}/api/{path}?ids={ids}")
        response_json = response.content.decode("utf-8")
        if response.status_code >= 300:
            logger.log_error(
                f"Failed to get {name}", {"response": response_json, "ids": ids}
            )
            return []
        return json.loads(response_json).get(result_key)
    except Exception as e:
        logger.log_exception(e, {"ids": ids})
        return []


def get_entities(host, entities, id_key, result_key, path, name):
    ids = ",".join(str(getattr(entity, id_key)) for entity in entities)
    return list_from_ids(host, ids, result_key, path, name)

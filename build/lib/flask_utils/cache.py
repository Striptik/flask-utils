from flask_redis import FlaskRedis

redis_client = FlaskRedis()


def get_cache(key: str):
    value = redis_client.get(key)
    return value.decode("utf-8") if value is not None else ""


def set_cache(key: str, value: str, expiration: int = None):
    return redis_client.set(key, value, expiration)


def del_cache(key: str):
    return redis_client.delete(key)

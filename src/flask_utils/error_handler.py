import enum as _enum
from flask import abort, jsonify
from werkzeug.exceptions import HTTPException, NotFound

from flask_utils.console import log
from flask_utils.i18n import translate

from .logger import log_error, log_exception


class ErrorTypeEnum(str, _enum.Enum):
    SERVER = "server"
    INTEGRITY = "integrity"
    BODY_VALIDATION = "body validation"
    SCHEMA_VALIDATION = "schema validation"


def handle_server_error(error, error_type):
    log(error)
    if error_type == ErrorTypeEnum.INTEGRITY:
        return (jsonify(error="Integrity - {}".format(str(error.orig)), metas={}), 400)
    elif error_type == ErrorTypeEnum.SCHEMA_VALIDATION:
        log_exception(error, error.messages)
        metas = error.messages
        metas.pop("traceback_lines")
        return (
            jsonify(error="Schema Validation - {}".format(str(error)), metas=metas),
            400,
        )
    else:
        code = 500
        log_exception(error, {})
        if isinstance(error, HTTPException):
            code = error.code
            return jsonify(error=format(str(error))), code
        return jsonify(error="Internal Error - {}".format(str(error))), code


def handle_error(message, metas={}, code=400):
    translated_message = translate(message)
    log_error(translated_message, metas)
    abort(code, translated_message)


def handle_not_found(entity, entity_name, entity_id):
    if not entity:
        log_error("{} {} not found".format(entity_name, entity_id))
        raise NotFound("{} not found".format(entity_name))

from datetime import datetime

from flask import request

from . import logger
from .error_handler import handle_not_found
from .search_params import parse_search_params
from .ms_request import reset_entity_cache


class GenericResourceClass:
    def __init__(
        self, repository, schema, list_schema, name, entity_name_key, result_key, env=None
    ):
        self.repository = repository
        self.schema = schema
        self.list_schema = list_schema
        self.name = name
        self.entity_name_key = entity_name_key
        self.result_key = result_key
        self.env = env

    def get(self, entity_id):
        entity = self.repository.get(entity_id)
        handle_not_found(entity, self.name, entity_id)
        return self.schema.dump(entity)

    def delete(self, entity_id, validator=None):
        entity = self.repository.get(entity_id)
        handle_not_found(entity, self.name, entity_id)
        if validator is not None:
            validator.validate(entity)
        self.repository.delete(entity_id)
        self.log_entity_change(
            entity_id, getattr(entity, self.entity_name_key, ""), entity, "deleted"
        )
        if self.env is not None:
            reset_entity_cache(name=self.name, env=self.env, _id=entity_id)
        return None, 204

    def update(self, entity_id, validator=None, **kwargs):
        entity_json = request.get_json()
        for key, value in kwargs.items():
            entity_json[key] = value
        updated_entity = self.schema.load(entity_json)
        existing_entity = self.repository.get(entity_id)
        handle_not_found(existing_entity, self.name, entity_id)
        updated_entity.updated_at = datetime.now()
        if validator is not None:
            validator.validate(updated_entity, existing_entity)
        self.repository.update(entity_id, updated_entity)
        self.log_entity_change(
            entity_id,
            getattr(existing_entity, self.entity_name_key, ""),
            updated_entity,
            "updated",
        )
        if self.env is not None:
            reset_entity_cache(name=self.name, env=self.env, _id=entity_id)
        return None, 204

    def create(self, validator=None, **kwargs):
        entity_json = request.get_json()
        for key, value in kwargs.items():
            entity_json[key] = value
        new_entity = self.schema.load(entity_json)
        new_entity.created_at = datetime.now()
        new_entity.updated_at = datetime.now()
        if validator is not None:
            validator.validate(new_entity)
        created_entity = self.repository.create(new_entity)
        self.log_entity_change(
            created_entity.id,
            getattr(created_entity, self.entity_name_key, ""),
            created_entity,
            "created",
        )
        return created_entity.id, 201

    def search(self, **kwargs):
        search_term, page, items_per_page, only_active = parse_search_params(request)
        entities, count = self.repository.search(
            search_term=search_term,
            page=page,
            items_per_page=items_per_page,
            only_active=only_active,
            **kwargs
        )
        result = {"count": count, self.result_key: self.list_schema.dump(entities)}
        return result

    def log_entity_change(self, entity_id, entity_name, new_entity, action):
        username = request.headers.get("username", default="")
        logger.log_info(
            "{} {} ({}) {} by {}".format(
                self.name, entity_id, entity_name, action, username
            ),
            {"id": entity_id, "data": self.schema.dump(new_entity)},
        )

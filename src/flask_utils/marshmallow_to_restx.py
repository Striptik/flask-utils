import marshmallow as ma
import flask_restx as restx
from flask_restx import Api
from typing import Callable, Union


__all__ = [
    "restx_fields",
    "marshmallow_to_restx_model"
]


restx_fields_mapper = {
    "Str": "String",
    "Bool": "Boolean",
    "Int": "Integer",
    "Email": "String",
    "Mapping": "Raw",
    "Dict": "Raw",
    "Tuple": "List",
    "UUID": "String",
    "Number": "Integer",
    "Decimal": "Float",
    "NaiveDateTime": "DateTime",
    "AwareDateTime": "DateTime",
    "Time": "DateTime",
    "Date": "DateTime",
    "TimeDelta": "DateTime",
    "URL": "String",
    "Url": "String",
    "IP": "String",
    "IPv4": "String",
    "IPv6": "String",
    "IPInterface": "String",
    "IPv4Interface": "String",
    "IPv6Interface": "String",
    "Constant": "String"
}


def restx_fields(
        description: str = None,
        enum: str = None,
        discriminator: str = None,
        min_length: int = None,
        max_length: int = None,
        pattern: str = None,
        attribute: str = None,
        default: Union[int, float, str, bool, dict, list] = None,
        title: str = None,
        required: bool = True,
        readonly: bool = False,
        example: str = None,
        mask: dict = None
):
    return {'restx_params': {
        'description': description,
        'enum': enum,
        'discriminator': discriminator,
        'min_length': min_length,
        'max_length': max_length,
        'pattern': pattern,
        'attribute': attribute,
        'default': default,
        'title': title,
        'required': required,
        'readonly': readonly,
        'example': example,
        'mask': mask
    }}


def get_marshmallow_field_type(ma_field: Callable) -> Union[str, None]:
    attr_name = getattr(type(ma_field), "__name__")
    if attr_name in restx_fields_mapper:
        return restx_fields_mapper[attr_name]
    return attr_name


def get_restx_params(ma_params: dict):
    restx_params = ma_params['metadata'].get('restx_params') or ma_params['metadata']
    return {
        'required': ma_params['required'],
        **restx_params,
    }


def get_field_data(ma_field):
    return {
        "params": get_restx_params(vars(ma_field)),
        "type": get_marshmallow_field_type(ma_field),
        "nested": None,
        "raw": ma_field
    }


def get_marshmallow_metadata(schema: Callable):
    marshmallow_metadata = {schema.__name__: {}}

    # Simple fields
    for field_name, ma_field in schema().declared_fields.items():
        marshmallow_metadata[schema.__name__][field_name] = get_field_data(ma_field)

    # Added recursion for nested fields
    for field_name, field_data in marshmallow_metadata[schema.__name__].items():

        if field_data['nested'] is None:

            if isinstance(field_data['raw'], ma.fields.Nested):
                marshmallow_metadata[schema.__name__][field_name]['nested'] = get_marshmallow_metadata(
                    field_data['raw'].nested)

            if isinstance(field_data['raw'], ma.fields.List):
                if hasattr(field_data['raw'].inner, 'nested'):
                    marshmallow_metadata[schema.__name__][field_name]['nested'] = get_marshmallow_metadata(
                        field_data['raw'].inner.nested)
                else:
                    marshmallow_metadata[schema.__name__][field_name]['inner'] = get_field_data(
                        field_data['raw'].inner
                    )

    return marshmallow_metadata


def get_restx_field(api: Api, ma_field_meta: dict, *, nested: bool = False):
    if nested:
        return restx.fields.Nested(
            api.model,
            skip_none=True,
            **ma_field_meta['params']
        )

    if ma_field_meta['type'] == "List" and "inner" in ma_field_meta:
        return restx.fields.List(
            getattr(restx.fields, ma_field_meta['inner']['type'])(**ma_field_meta['inner']['params']),
            skip_none=True,
            **ma_field_meta['params']
        )

    restx_field = getattr(restx.fields, ma_field_meta['type'])
    restx_field_instance = restx_field(
        required=ma_field_meta['params'].get('required', False),
        skip_none=True
    )
    return restx_field_instance


def ma_metadata_to_restx_model(api: Api, ma_metadata: dict):
    restx_model = {}

    for schema_name, mameta in ma_metadata.items():

        for field_name, ma_field_meta in mameta.items():

            if ma_field_meta['nested'] is None:
                restx_model[field_name] = get_restx_field(api, ma_field_meta)
            else:
                restx_model[field_name] = ma_metadata[schema_name][field_name]

    # Added recursion for nested fields
    for field_name, field_instance in restx_model.items():

        if isinstance(field_instance, dict):

            if 'inner' in field_instance:
                restx_model[field_name] = get_restx_field(api, ma_field_meta)

            if field_instance['type'] == 'Nested':
                restx_model[field_name] = get_restx_field(api, field_instance, nested=True)
                restx_model[field_name].model = ma_metadata_to_restx_model(api, field_instance['nested'])

            if field_instance['type'] == 'List' and field_instance['nested'] is not None:
                restx_model[field_name] = restx.fields.List(
                    restx.fields.Nested(ma_metadata_to_restx_model(api, field_instance['nested']), skip_none=True),
                    **ma_field_meta['params'],
                )

    return api.model(schema_name, restx_model)


def marshmallow_to_restx_model(api: restx.Api, schema: Callable):
    ma_metadata = get_marshmallow_metadata(schema)
    restx_model = ma_metadata_to_restx_model(api, ma_metadata)
    return restx_model

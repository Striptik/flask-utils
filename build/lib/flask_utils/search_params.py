from flask_restx import fields, inputs


def get_expected_search_params(with_active_filter=False):
    search_params = {
        "searchTerm": {
            "description": "search term",
            "type": "string",
            "required": False,
            "default": "",
        },
        "page": {"description": "page", "type": "number", "default": 1},
        "itemsPerPage": {
            "description": "items per page",
            "type": "number",
            "default": 10,
        },
    }
    if with_active_filter:
        search_params["onlyActive"] = {
            "description": "should return only active users",
            "type": "boolean",
            "default": False,
        }
    return search_params


def parse_search_params(request):
    search_term = request.args.get("searchTerm", default="")
    page = int(request.args.get("page", default=1))
    items_per_page = int(request.args.get("itemsPerPage", default=10))
    only_active = request.args.get("onlyActive", default=False, type=inputs.boolean)
    return [search_term, page, items_per_page, only_active]


def format_search_term(search_term):
    return "%" + search_term + "%"


def get_list_marshal_with(api, key: str, entity_fields):
    return api.model(
        key,
        {
            "count": fields.Integer(required=False),
            key: fields.List(fields.Nested(entity_fields, skip_none=True)),
        },
    )

def get_search_result(query, page, items_per_page, only_active=False):
    query = query.filter_by(is_active=True) if only_active else query
    return (
        (
            query.offset((items_per_page or 10) * ((page or 1) - 1))
            .limit((items_per_page or 10))
            .all()
        ),
        query.count(),
    )


def check_int(search_term: str):
    try:
        int(search_term)
        return True
    except ValueError:
        return False

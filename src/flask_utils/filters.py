def filter_not_none(input_dict):
    if input_dict is None:
        return None
    return {key: value for (key, value) in input_dict.items() if value}

def flatten_json(json_obj, prefix='', sep='_', flatten_lists=False):
    flattened = {}
    for key, value in json_obj.items():
        new_key = prefix + key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key + sep))
        elif flatten_lists and isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened.update(flatten_json(item, new_key + sep + str(i) + sep))
                else:
                    flattened[new_key + sep + str(i)] = item
        else:
            flattened[new_key] = value
    return flattened

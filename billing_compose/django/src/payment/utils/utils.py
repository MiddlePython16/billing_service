def get_json_from_permissions(items):
    json_data = {}
    for item in items:
        for permission in item.permissions.all():
            if permission.name in json_data:
                json_data[permission.name].append(permission.json_data)
                continue
            json_data[permission.name] = [permission.json_data]
    return json_data

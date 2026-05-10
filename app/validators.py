def validate_create_user(data):
    if not data:
        return "request body is required"

    if "name" not in data or "email" not in data:
        return "name and email are required"

    if not str(data["name"]).strip():
        return "name cannot be empty"

    if not str(data["email"]).strip():
        return "email cannot be empty"

    return None


def validate_update_user(data):
    if not data:
        return "request body is required"

    if "name" not in data and "email" not in data:
        return "name or email is required"

    if "name" in data and not str(data["name"]).strip():
        return "name cannot be empty"

    if "email" in data and not str(data["email"]).strip():
        return "email cannot be empty"

    return None
from app.validators import validate_create_user, validate_update_user


def test_validate_create_user_success():
    data = {
        "name": "Juan",
        "email": "juan@test.com"
    }

    assert validate_create_user(data) is None


def test_validate_create_user_without_email():
    data = {
        "name": "Juan"
    }

    assert validate_create_user(data) == "name and email are required"


def test_validate_update_user_success():
    data = {
        "name": "Juan Modificado"
    }

    assert validate_update_user(data) is None
from app.main import users


def test_users_is_list():
    assert isinstance(users, list)
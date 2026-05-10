import pytest
from app.main import app
from app.db import get_connection, init_db


@pytest.fixture(autouse=True)
def reset_database():
    init_db()
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE users RESTART IDENTITY;")
    finally:
        conn.close()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["database"] == "ok"


def test_get_users_empty(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json == []


def test_create_user(client):
    response = client.post("/users", json={
        "name": "Juan",
        "email": "juan@test.com"
    })

    assert response.status_code == 201
    assert response.json["id"] == 1
    assert response.json["name"] == "Juan"


def test_get_user_by_id(client):
    create_response = client.post("/users", json={
        "name": "Juan",
        "email": "juan@test.com"
    })

    user_id = create_response.json["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json["name"] == "Juan"


def test_update_user(client):
    create_response = client.post("/users", json={
        "name": "Juan",
        "email": "juan@test.com"
    })

    user_id = create_response.json["id"]

    response = client.put(f"/users/{user_id}", json={
        "name": "Juan Modificado",
        "email": "juan.modificado@test.com"
    })

    assert response.status_code == 200
    assert response.json["name"] == "Juan Modificado"
    assert response.json["email"] == "juan.modificado@test.com"


def test_delete_user(client):
    create_response = client.post("/users", json={
        "name": "Juan",
        "email": "juan@test.com"
    })

    user_id = create_response.json["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json["message"] == "user deleted"

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_user(client):
    response = client.post("/users", json={
        "name": "Juan",
        "email": "juan@test.com"
    })

    assert response.status_code == 201
    assert response.json["name"] == "Juan"
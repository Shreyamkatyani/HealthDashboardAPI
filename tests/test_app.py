import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_environment_default(client, monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    response = client.get("/environment")
    assert response.status_code == 200
    assert response.get_json() == {"environment": "development"}


def test_environment_custom(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "staging")
    response = client.get("/environment")
    assert response.status_code == 200
    assert response.get_json() == {"environment": "staging"}

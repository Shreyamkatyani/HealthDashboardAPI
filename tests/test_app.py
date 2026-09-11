import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert data["version"] == "1.0.0"


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


from app import app


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()
    assert data["application"] == "DevOps Status API"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_unknown_endpoint():
    client = app.test_client()
    response = client.get("/unknown")

    assert response.status_code == 404

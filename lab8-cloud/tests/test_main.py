from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_item():
    response = client.post("/items", json={"name": "Caderno", "price": 12.5})
    assert response.status_code == 200
    assert response.json() == {
        "created": {"name": "Caderno", "price": 12.5}
    }

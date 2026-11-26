from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_rooms_returns_empty_list():
    response = client.get("/api/v1/rooms")
    assert response.status_code == 200
    assert response.json() == []

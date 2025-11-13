import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_create_user():
    user = {
        "email": f"user_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Usuário Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }

    response = client.post("/api/users/", json=user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["email"] == user["email"]

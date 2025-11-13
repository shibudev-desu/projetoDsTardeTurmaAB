import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_delete_user():
    user = {
        "email": f"delete_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Ana Teste Delete",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }

    create_response = client.post("/api/users/", json=user)
    assert create_response.status_code == 200, create_response.text
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully"

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_user():
    user = {
        "id": 2,
        "email": "maria@gmail.com",
        "username": "mariazinha",
        "name": "Maria Silva",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }
    response = client.post("/api/users/", json=user)

    if response.status_code != 200:
        print(f" Erro {response.status_code} ao criar usuário.")
        print("Resposta completa:", response.json())

        assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Maria Silva"
    assert data["email"] == "maria@gmail.com"
    assert data["username"] == "mariazinha"
    assert data["password_hash"] == "senha123"
    assert "id" in data
    assert isinstance(data["id"], int)

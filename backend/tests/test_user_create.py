import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_create_user():
    """Testa a criação de um usuário (POST /api/users/)"""
    
    payload = {
        "email": f"user_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Usuário Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }

    response = client.post("/api/users/", json=payload)

    # Verifica se a rota existe
    assert response.status_code != 404, (
        f"\n❌ ERRO 404 — Rota /api/users/ não encontrada.\n"
        f"Resposta: {response.text}"
    )

    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 200, (
        f"\n❌ Código inesperado: {response.status_code}\n"
        f"Resposta: {response.text}"
    )

    data = response.json()

    # Validações do resultado
    assert "id" in data, "A resposta não contém o campo 'id'."
    assert data.get("email") == payload["email"], "O e-mail retornado está incorreto."
    assert data.get("username") == payload["username"], "O username retornado está incorreto."
    assert data.get("type") == payload["type"], "O tipo retornado está incorreto."

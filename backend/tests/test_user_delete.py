import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_delete_user():
    """Testa a exclusão de um usuário (DELETE /api/users/{id})"""

    # --- Criação do usuário temporário ---
    payload = {
        "email": f"delete_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Ana Teste Delete",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }

    create_response = client.post("/api/users/", json=payload)
    assert create_response.status_code == 200, (
        f"\n❌ Falha ao criar usuário para teste.\n"
        f"Resposta: {create_response.text}"
    )

    user_id = create_response.json().get("id")
    assert user_id is not None, "❌ O usuário criado não retornou um ID."

    # --- Exclusão do usuário ---
    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code != 404, (
        f"\n❌ Rota /api/users/{user_id} não encontrada.\n"
        f"Resposta: {delete_response.text}"
    )

    assert delete_response.status_code == 200, (
        f"\n❌ DELETE retornou o status {delete_response.status_code}, esperado 200.\n"
        f"Resposta: {delete_response.text}"
    )

    data = delete_response.json()

    # Garante que a mensagem está presente
    assert "message" in data, "❌ A resposta não contém o campo 'message'."

    # Valida o texto da mensagem
    assert data["message"] == "User deleted successfully", (
        f"\n❌ Mensagem inesperada ao deletar usuário.\n"
        f"Recebido: {data['message']}"
    )

    # --- Confirma que o usuário foi realmente apagado ---
    confirm_response = client.get(f"/api/users/{user_id}")
    assert confirm_response.status_code == 404, (
        "\n❌ O usuário ainda está acessível após o DELETE."
    )

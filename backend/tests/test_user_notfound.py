from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_delete_nonexistent_user():
    """Testa a exclusão de um usuário que não existe (DELETE /api/users/999)"""

    response = client.delete("/api/users/999")

    # Caso a API esteja seguindo corretamente o padrão HTTP
    if response.status_code == 404:
        print("\n⚠️ Usuário não encontrado (status 404).")
        print("Resposta:", response.json())

        data = response.json()
        # A API pode retornar 'detail' (padrão FastAPI) ou 'error'
        assert any(k in data for k in ("detail", "error")), (
            "A resposta 404 não trouxe 'detail' nem 'error'."
        )
        return

    # Caso a API esteja retornando 200 com mensagem de erro
    assert response.status_code == 200, (
        f"Status inesperado: {response.status_code}. Resposta: {response.text}"
    )

    data = response.json()
    assert "error" in data, "A resposta não contém o campo 'error'."
    assert data["error"] == "User not found", "Mensagem de erro incorreta."

    # Garante que a listagem continua funcionando
    list_response = client.get("/api/users/")
    assert list_response.status_code == 200, "Falha ao acessar /api/users/ após o delete."
    assert isinstance(list_response.json(), list), "A rota /api/users/ não retornou uma lista."

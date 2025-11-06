from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete_nonexistent_user():
    response = client.delete("/api/users/999")

    if response.status_code == 404:
        print("Erro 404! Usuário não encontrado.")
        print("Response content:", response.json())
        data = response.json()
        assert "detail" in data or "error" in data
        return

    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "User not found"

    list_response = client.get("/api/users/") 
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
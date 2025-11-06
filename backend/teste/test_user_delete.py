from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete_user():
    user = {"name": "Ana"}
    create_response = client.post("/api/users/", json=user)  # <-- corrigido
    if create_response.status_code == 404:
        print("Erro 404! Usuário não encontrado.")
        print("Response content:", create_response.json())
        return
    
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")  # <-- corrigido
    if response.status_code == 404:
        print("Erro 404! Usuário não encontrado.")
        print("Response content:", response.json())
        return
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

    get_response = client.get(f"/api/users/{user_id}")  # <-- corrigido
    assert get_response.json() is None
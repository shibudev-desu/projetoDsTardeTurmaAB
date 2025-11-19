from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_user():
    user = {"name": "Pedro"}
    create_response = client.post("/users/", json=user)
    user_id = create_response.json()["id"]

    updated_user = {"name": "Pedro Atualizado"}
    response = client.put(f"/users/{user_id}", json=updated_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated"

    get_response = client.get(f"/users/{user_id}")
    assert get_response.json()["name"] == "Pedro Atualizado"
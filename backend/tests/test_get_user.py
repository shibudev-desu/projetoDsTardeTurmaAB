from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user():
    user = {"name": "Jo�o"}
    create_response = client.post("/users/", json=user)
    created_user = create_response.json()

    user_id = created_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["name"] == "Jo�o"
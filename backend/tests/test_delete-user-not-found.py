from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete_nonexistent_user():
    response = client.delete("/users/999")
    assert response.status_code == 200
    assert response.json()["error"] == "User not found"
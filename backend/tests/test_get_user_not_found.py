from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_nonexistent_user():
    response = client.get("/users/999")
    assert response.status_code == 200
    assert response.json() is None
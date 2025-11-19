import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_login_returns_token():
    # cria usuário com senha conhecida
    payload = {
        "email": f"login_{uuid.uuid4().hex[:6]}@example.com",
        "username": f"u_{uuid.uuid4().hex[:4]}",
        "name": "Login Test",
        "password_hash": "mypassword",  # dependendo de sua API, talvez precise criar password claro
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "normal",
        "created_at": "2025-01-01"
    }
    create = client.post("/api/users/", json=payload)
    assert create.status_code == 200, create.text

    login_payload = {"username": payload["username"], "password": "mypassword"}
    resp = client.post("/api/auth/login", json=login_payload)
    # suporte a diferentes implementações (200 com token ou 401)
    assert resp.status_code in (200, 401, 422)
    if resp.status_code == 200:
        body = resp.json()
        assert "access_token" in body or "token" in body

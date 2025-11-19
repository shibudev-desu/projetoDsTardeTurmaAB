from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_all_users_returns_list():
    resp = client.get("/api/users/")
    assert resp.status_code == 200, f"Esperado 200, recebeu {resp.status_code}: {resp.text}"
    assert isinstance(resp.json(), list), "A rota /api/users/ deve retornar uma lista"

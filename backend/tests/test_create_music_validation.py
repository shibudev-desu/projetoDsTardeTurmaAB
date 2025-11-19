import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_music_missing_required_fields():
    # falta title e artist_id
    payload = {"duration": 120}
    resp = client.post("/api/musics/", json=payload)
    # API REST bem feita retorna 400 para payload inválido
    assert resp.status_code in (400, 422), f"Esperado 400/422, recebido {resp.status_code}"
    # body deve explicar o erro
    assert isinstance(resp.json(), dict)

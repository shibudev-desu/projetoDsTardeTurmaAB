import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_music_by_id():
    # Cria um usuário/artista simples (se necessário)
    user = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@example.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artist For Music",
        "password_hash": "senha",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }
    uresp = client.post("/api/users/", json=user)
    assert uresp.status_code == 200, uresp.text
    artist_id = uresp.json()["id"]

    music = {
        "title": "Track Test",
        "artist_id": artist_id,
        "file_url": f"https://ex/{uuid.uuid4().hex}.mp3",
        "duration": 200,
        "genre": "Test",
        "created_at": "2025-01-01"
    }
    mresp = client.post("/api/musics/", json=music)
    assert mresp.status_code == 200, mresp.text
    mid = mresp.json()["id"]

    get = client.get(f"/api/musics/{mid}")
    assert get.status_code == 200
    data = get.json()
    assert data["id"] == mid
    assert data["title"] == "Track Test"

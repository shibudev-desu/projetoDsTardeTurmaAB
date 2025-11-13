import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_all_musics():
    response = client.get("/api/musics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_music():
    user = {
        "email": f"user_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Usuário Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

    user_response = client.post("/api/users/", json=user)
    assert user_response.status_code == 200, user_response.text
    user_id = user_response.json()["id"]

    music = {
        "title": f"Song {uuid.uuid4().hex[:6]}",
        "artist_id": user_id,
        "file_url": f"https://example.com/{uuid.uuid4().hex[:8]}.mp3",
        "duration": 180,
        "genre": "Pop",
        "created_at": "2025-01-01"
    }

    response = client.post("/api/musics/", json=music)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["title"].startswith("Song")

import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_all_musics():
    response = client.get("/api/musics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_music():
    music = {
        "title": f"Song {uuid.uuid4().hex[:6]}",
        "artist_id": "test_artist_id_123",  # substitua por ID válido se necessário
        "file_url": f"https://example.com/{uuid.uuid4().hex[:8]}.mp3",
        "cover_url": "https://example.com/cover.jpg",
        "duration": 180,
        "genre": "Pop",
        "created_at": "2025-01-01"
    }

    response = client.post("/api/musics/", json=music)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["title"].startswith("Song")

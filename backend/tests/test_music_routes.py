import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


# ---------------------------
#  Helpers (Factories)
# ---------------------------

def make_user(**overrides):
    base = {
        "email": f"user_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:4]}",
        "name": "Usuário Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }
    base.update(overrides)
    return base


def make_music(artist_id: int, **overrides):
    base = {
        "title": f"Song {uuid.uuid4().hex[:6]}",
        "artist_id": artist_id,
        "file_url": f"https://example.com/{uuid.uuid4().hex[:8]}.mp3",
        "duration": 180,
        "genre": "Pop",
        "created_at": "2025-01-01"
    }
    base.update(overrides)
    return base


# ---------------------------
#           TESTS
# ---------------------------

def test_get_all_musics():
    response = client.get("/api/musics/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_music():
    # Create artist
    user_payload = make_user()
    user_resp = client.post("/api/users/", json=user_payload)
    assert user_resp.status_code == 200, user_resp.text
    artist_id = user_resp.json()["id"]

    # Create music
    music_payload = make_music(artist_id=artist_id)
    resp = client.post("/api/musics/", json=music_payload)

    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert "id" in data
    assert data["title"].startswith("Song")
    assert data["artist_id"] == artist_id
    assert data["duration"] == 180
    assert data["genre"] == "Pop"
    assert data["file_url"].startswith("https://example.com/")

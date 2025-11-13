import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_artists():
    response = client.get("/api/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_artist():
    artist = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artista Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

    response = client.post("/api/artists/", json=artist)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data


def test_get_artist_by_id():
    artist = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artista Get ID",
        "password_hash": "senha123",
        "latitude": 1.0,
        "longitude": 1.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

    create_response = client.post("/api/artists/", json=artist)
    assert create_response.status_code == 200, create_response.text
    artist_id = create_response.json()["id"]

    response = client.get(f"/api/artists/{artist_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == artist_id


def test_update_artist():
    artist = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artista Update",
        "password_hash": "senha123",
        "latitude": 2.0,
        "longitude": 2.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

    create_response = client.post("/api/artists/", json=artist)
    artist_id = create_response.json()["id"]

    update_data = {"name": "Artista Atualizado"}
    response = client.put(f"/api/artists/{artist_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Artista Atualizado"


def test_delete_artist():
    artist = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artista Delete",
        "password_hash": "senha123",
        "latitude": 3.0,
        "longitude": 3.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

    create_response = client.post("/api/artists/", json=artist)
    artist_id = create_response.json()["id"]

    response = client.delete(f"/api/artists/{artist_id}")
    assert response.status_code == 200
    assert "message" in response.json()

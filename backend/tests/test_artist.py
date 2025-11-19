import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


# ---------------------------
#  Helper: Factory de artista
# ---------------------------
def make_artist(**overrides):
    base = {
        "email": f"artist_{uuid.uuid4().hex[:6]}@gmail.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artista Teste",
        "password_hash": "senha123",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }
    base.update(overrides)
    return base


# ---------------------------
#         TESTES
# ---------------------------

def test_get_artists():
    response = client.get("/api/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list), "O retorno deve ser uma lista"


def test_create_artist():
    artist = make_artist()

    response = client.post("/api/artists/", json=artist)
    assert response.status_code == 200, response.text

    data = response.json()
    assert "id" in data
    assert data["email"] == artist["email"]
    assert data["username"] == artist["username"]


def test_get_artist_by_id():
    artist = make_artist(name="Artista Get ID")

    create_response = client.post("/api/artists/", json=artist)
    assert create_response.status_code == 200
    artist_id = create_response.json()["id"]

    response = client.get(f"/api/artists/{artist_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == artist_id
    assert data["name"] == "Artista Get ID"


def test_update_artist():
    artist = make_artist(name="Artista Update")
    create_response = client.post("/api/artists/", json=artist)
    artist_id = create_response.json()["id"]

    update_data = {"name": "Artista Atualizado"}

    response = client.put(f"/api/artists/{artist_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Artista Atualizado"


def test_delete_artist():
    artist = make_artist(name="Artista Delete")
    create_response = client.post("/api/artists/", json=artist)
    artist_id = create_response.json()["id"]

    response = client.delete(f"/api/artists/{artist_id}")
    assert response.status_code == 200
    json_data = response.json()
    assert "message" in json_data
    assert "excluído" in json_data["message"].lower()

import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def make_artist_payload():
    return {
        "email": f"artist_{uuid.uuid4().hex[:6]}@example.com",
        "username": f"art_{uuid.uuid4().hex[:4]}",
        "name": "Artist Test",
        "password_hash": "senha",
        "latitude": 0.0,
        "longitude": 0.0,
        "type": "artist",
        "created_at": "2025-01-01"
    }

def test_artist_crud_flow():
    # create
    payload = make_artist_payload()
    c = client.post("/api/artists/", json=payload)
    assert c.status_code == 200, c.text
    aid = c.json()["id"]

    # get
    g = client.get(f"/api/artists/{aid}")
    assert g.status_code == 200
    assert g.json()["id"] == aid

    # update
    up = client.put(f"/api/artists/{aid}", json={"name": "Novo Nome"})
    assert up.status_code == 200
    assert up.json().get("name") == "Novo Nome"

    # delete
    d = client.delete(f"/api/artists/{aid}")
    assert d.status_code == 200

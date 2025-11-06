from fastapi.testclient import TestClient
from  backend.main import app

client = TestClient(app)

def test_get_artists():
    response = client.get("/api/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_artist():
    new_artist = {"name": "Anitta"}
    response = client.post("/api/artists/", json=new_artist)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Anitta"

def test_get_artist_by_id():
    create_response = client.post("/api/artists/", json={"name": "Alok"})
    artist_id = create_response.json()["id"]

    response = client.get(f"/api/artists/{artist_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == artist_id
    assert data["name"] == "Alok"

def test_update_artist():
    create_response = client.post("/api/artists/", json={"name": "Luan"})
    artist_id = create_response.json()["id"]

    update_response = client.put(f"/api/artists/{artist_id}", json={"name": "Luan Santana"})
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Artist updated"

def test_delete_artist():
    create_response = client.post("/api/artists/", json={"name": "Iza"})
    artist_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/artists/{artist_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Artist deleted"
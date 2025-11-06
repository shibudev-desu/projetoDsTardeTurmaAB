from fastapi import APIRouter
from app.db.fake_db import fake_db
from app.models import Artist

router = APIRouter()

@router.get("/")
def get_artists():
    return fake_db["artists"]

@router.post("/")
def create_artist(artist: Artist):
    new_artist = {
        "id": len(fake_db["artists"]) + 1,
        "name": artist.name
    }
    fake_db["artists"].append(new_artist)
    return new_artist

@router.get("/{artist_id}")
def get_artist(artist_id: int):
    return next((a for a in fake_db["artists"] if a["id"] == artist_id), None)

@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: Artist):
    index = next((i for i, a in enumerate(fake_db["artists"]) if a["id"] == artist_id), None)
    if index is None: return None
    fake_db["artists"][index]["name"] = artist.name
    return {"message": "Artist updated"}

@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
    index = next((i for i, a in enumerate(fake_db["artists"]) if a["id"] == artist_id), None)
    if index is None: return None
    del fake_db["artists"][index]
    return {"message": "Artist deleted"}

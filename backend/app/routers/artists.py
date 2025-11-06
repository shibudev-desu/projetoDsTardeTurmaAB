"""
CRUD de artistas usando FastAPI e banco fake em memória.
"""

from fastapi import APIRouter
from app.models import Artist
from app.db.fake_db import fake_db

router = APIRouter()

# GET - Buscar todos artistas
@router.get("/")
def get_artists():
    return fake_db['artists']

# GET - Buscar artista por ID
@router.get("/{artist_id}")
def get_artist(artist_id: int):
    artist = next((artist for artist in fake_db["artists"] if artist["id"] == artist_id), None)

    if not artist:
        return {"error": "Artist not found"}

    return artist

# POST - Criar artista
@router.post("/")
def create_artist(artist: Artist):
    new_artist = {
        "id": len(fake_db['artists']) + 1,
        "name": artist.name,
        "email": artist.email,
        "password": artist.password,
        "bio": artist.bio,
        "musics": artist.musics,
    }

    fake_db['artists'].append(new_artist)

    return new_artist

# PUT - Atualizar artista
@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: Artist):

    index = next((i for i, a in enumerate(fake_db['artists']) if a["id"] == artist_id), None)

    if index is None:
        return {"error": "Artist not found"}

    fake_db['artists'][index] = {
        "id": artist_id,
        "name": artist.name,
        "email": artist.email,
        "password": artist.password,
        "bio": artist.bio,
        "musics": artist.musics,
    }

    return {"message": "Artist updated"}

# DELETE - Deletar artista
@router.delete("/{artist_id}")
def delete_artist(artist_id: int):

    index = next((i for i, a in enumerate(fake_db['artists']) if a["id"] == artist_id), None)

    if index is None:
        return {"error": "Artist not found"}

    del fake_db['artists'][index]

    return {"message": "Artist deleted"}

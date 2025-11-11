from fastapi import APIRouter
from app.db.fake_db import fake_db

router = APIRouter()

# GET "/" -> lista todas as músicas
@router.get("/")
def get_all_musics():
    return fake_db["musics"]

# POST "/" -> cria uma nova música
@router.post("/")
def create_music_route(music: dict):
    new_music = {
        "id": len(fake_db["musics"]) + 1,
        "title": music.get("title")
    }
    fake_db["musics"].append(new_music)
    return new_music

# GET "/{music_id}" -> retorna música por ID
@router.get("/{music_id}")
def get_specific_music(music_id: int):
    music = next((m for m in fake_db["musics"] if m["id"] == music_id), None)
    return music or {}

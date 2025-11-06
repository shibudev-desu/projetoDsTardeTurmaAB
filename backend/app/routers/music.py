from fastapi import APIRouter
from app.models import Music
from app.db.fake_db import fake_db

router = APIRouter()

@router.get("/")
def get_all_musics():
    return fake_db["musics"]

@router.post("/")
def create_music(music: Music):
    new_music = {
        "id": len(fake_db["musics"]) + 1,
        "title": music.title
    }
    fake_db["musics"].append(new_music)
    return new_music

@router.get("/{music_id}")
def get_music(music_id: int):
    music = next((m for m in fake_db["musics"] if m["id"] == music_id), None)
    if not music:
        return {"error": "Music not found"}
    return music

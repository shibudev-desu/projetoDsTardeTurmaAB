from fastapi import APIRouter
from app.db.fake_db import fake_db
from app.models import Music

router = APIRouter()

@router.get("/")
def get_all_musics():
    return fake_db["musics"]

@router.post("/")
def create_music(music: Music):
    new_music = {
        "id": len(fake_db["musics"]) + 1,
        "title": music.title,
        "description": music.description,
        "artist_id": music.artist_id,
        "duration": music.duration,
        "posted_at": music.posted_at
    }
    fake_db["musics"].append(new_music)
    return new_music

@router.get("/{music_id}")
def get_music(music_id: int):
    return next((m for m in fake_db["musics"] if m["id"] == music_id), None)

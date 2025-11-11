from fastapi import APIRouter, HTTPException
from app.models import Music
from app.db.supabase import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_all_musics():
    response = supabase.table("musics").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data

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

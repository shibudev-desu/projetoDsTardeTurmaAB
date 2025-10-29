from fastapi import APIRouter
from app.models import Music
from app.db.fake_db import fake_db
from app.db.supabase_client import get_supabase

router = APIRouter()

@router.get("/get_music")
def get_music():
    return fake_db['musics']

@router.get("/selectmusic")
def get_musics():
    supabase = get_supabase()
    response = supabase.table("musics").select("*").execute()
    return response.data  

@router.get("/musics/{music_ids}")
def get_music_by_id(music_ids: int):
    supabase = get_supabase()
    response = supabase.table("musics").select("*").eq("id", music_ids).execute()
    if response.data:
        return response.data[0]
    return {"error": "Music not found"}

@router.post("/")
def create_music(music: Music):
    new_music = {"id": len(fake_db) + 1, "title": music.title}
    fake_db.musics.append(new_music)
    return new_music

@router.put("/{music_id}")
def update_music(music_id: int, music: Music):
    if music_id > len(fake_db):
        return {"error": "Music not found"}
    fake_db.musics[music_id - 1] = {"id": music_id, "title": music.title}
    return {"message": "Music updated"}

@router.delete("/{music_id}")
def delete_music(music_id: int):
    if music_id > len(fake_db):
        return {"error": "Music not found"}
    del fake_db.musics[music_id - 1]
    return {"message": "Music deleted"}
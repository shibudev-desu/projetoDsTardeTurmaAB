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

@router.get("/musics/{music_id}")
def get_music_by_id(music_id: int):
    supabase = get_supabase()
    response = supabase.table("musics").select("*").eq("id", music_id).execute()
    if response.data:
        return response.data[0]
    return {"error": "Music not found"}

@router.post("/musics")
def create_music(music: Music):
    supabase = get_supabase()
    new_music = {
        "title": music.title,
        "description": music.description,
        "artist_id": music.artist_id,
        "duration": music.duration,
        "audio_url": music.audio_url,
        "lyrics": music.lyrics,
        "genre": music.genre,
        
    }
    response = supabase.table("musics").insert(new_music).execute()
    if response.data:
        return response.data[0]
    return {"error": "Failed to create music"}

@router.put("/musics/{music_id}")
def update_music(music_id: int, music: Music):
    supabase = get_supabase()
    updated_data = {
        "title": music.title,
        "description": music.description,
        "artist_id": music.artist_id,
        "duration": music.duration,
        "audio_url": music.audio_url,
        "lyrics": music.lyrics,
        "genre": music.genre,
    }
    response = supabase.table("musics").update(updated_data).eq("id", music_id).execute()
    if response.data:
        return {"message": "Music updated successfully"}
    return {"error": "Music not found"}

@router.delete("/musics/{music_id}")
def delete_music(music_id: int):
    supabase = get_supabase()
    response = supabase.table("musics").delete().eq("id", music_id).execute()
    if response.data:
        return {"message": "Music deleted successfully"}
    return {"error": "Music not found"}
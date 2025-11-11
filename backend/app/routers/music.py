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
    data = {
        "title": music.title,
        "description": music.description,
        "artist_id": music.artist_id,
        "duration": music.duration,
        "posted_at": music.posted_at
    }
    response = supabase.table("musics").insert(data).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data

@router.get("/{music_id}")
def get_music(music_id: int):
    response = supabase.table("musics").select("*").eq("id", music_id).single().execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    if not response.data:
        raise HTTPException(status_code=404, detail="Music not found")
    return response.data

@router.put("/{music_id}")
def update_music(music_id: int, music: Music):
    existing = supabase.table("musics").select("*").eq("id", music_id).single().execute()
    if existing.error:
        raise HTTPException(status_code=500, detail=str(existing.error))
    if not existing.data:
        raise HTTPException(status_code=404, detail="Music not found")

    data = {
        "title": music.title,
        "description": music.description,
        "artist_id": music.artist_id,
        "duration": music.duration,
        "posted_at": music.posted_at
    }
    response = supabase.table("musics").update(data).eq("id", music_id).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return {"message": "Music updated", "data": response.data}

@router.delete("/{music_id}")
def delete_music(music_id: int):
    existing = supabase.table("musics").select("*").eq("id", music_id).single().execute()
    if existing.error:
        raise HTTPException(status_code=500, detail=str(existing.error))
    if not existing.data:
        raise HTTPException(status_code=404, detail="Music not found")

    response = supabase.table("musics").delete().eq("id", music_id).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return {"message": "Music deleted"}
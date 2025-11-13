from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_musics():
    response = supabase.table("musics").select("*").execute()
    return response.data


@router.get("/{music_id}")
def get_music_by_id(music_id: int):
    response = supabase.table("musics").select("*").eq("id", music_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Music not found")
    return response.data[0]


@router.post("/")
def create_music(music: dict):
    # verifica se o artista existe e é do tipo "artist"
    artist_check = (
        supabase.table("users")
        .select("*")
        .eq("id", music["artist_id"])
        .eq("type", "artist")
        .execute()
    )
    if not artist_check.data:
        raise HTTPException(status_code=400, detail="Invalid artist_id")

    response = supabase.table("musics").insert(music).execute()
    return response.data[0]


@router.put("/{music_id}")
def update_music(music_id: int, music: dict):
    response = supabase.table("musics").update(music).eq("id", music_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Music not found")
    return response.data[0]


@router.delete("/{music_id}")
def delete_music(music_id: int):
    response = supabase.table("musics").delete().eq("id", music_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Music not found")
    return {"message": "Music deleted successfully"}

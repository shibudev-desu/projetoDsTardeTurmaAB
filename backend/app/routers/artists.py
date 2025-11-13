from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_artists():
    response = supabase.table("users").select("*").eq("type", "artist").execute()
    return response.data


@router.get("/{artist_id}")
def get_artist_by_id(artist_id: int):
    response = (
        supabase.table("users")
        .select("*")
        .eq("id", artist_id)
        .eq("type", "artist")
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return response.data[0]


@router.post("/")
def create_artist(artist: dict):
    artist["type"] = "artist"
    response = supabase.table("users").insert(artist).execute()
    return response.data[0]


@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: dict):
    response = (
        supabase.table("users")
        .update(artist)
        .eq("id", artist_id)
        .eq("type", "artist")
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return response.data[0]


@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
    response = (
        supabase.table("users")
        .delete()
        .eq("id", artist_id)
        .eq("type", "artist")
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted successfully"}

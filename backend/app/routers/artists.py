from fastapi import APIRouter, HTTPException
from app.models import Artist
from app.db.supabase import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_artists():
    response = supabase.table("artists").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data

@router.post("/")
def create_artist(artist: Artist):
    response = supabase.table("artists").insert({"name": artist.name}).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data


@router.get("/{artist_id}")
def get_artist(artist_id: int):
    return next((a for a in fake_db["artists"] if a["id"] == artist_id), None)

@router.put("/{artist_id}")
def update_artist(artist_id: int, artist: Artist):
    index = next((i for i, a in enumerate(fake_db["artists"]) if a["id"] == artist_id), None)
    if index is None: return None
    fake_db["artists"][index]["name"] = artist.name
    return {"message": "Artist updated"}

@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
    index = next((i for i, a in enumerate(fake_db["artists"]) if a["id"] == artist_id), None)
    if index is None: return None
    del fake_db["artists"][index]
    return {"message": "Artist deleted"}

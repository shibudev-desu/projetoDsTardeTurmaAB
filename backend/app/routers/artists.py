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
    response = supabase.table("artists").select("*").eq("id", artist_id).single().execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    if not response.data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return response.data


@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
    index = next((i for i, a in enumerate(fake_db["artists"]) if a["id"] == artist_id), None)
    if index is None: return None
    del fake_db["artists"][index]
    return {"message": "Artist deleted"}

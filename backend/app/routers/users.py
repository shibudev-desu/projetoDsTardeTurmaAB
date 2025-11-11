from fastapi import APIRouter, HTTPException
from app.models import User
from app.db.supabase_client import get_supabase

router = APIRouter()
supabase = get_supabase()

@router.get("/")
def get_users():
    response = supabase.table("users").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data

@router.post("/")
def create_user(user: User):
    response = supabase.table("users").insert({
        "name": user.name,
        "email": getattr(user, "email", None),
        "username": getattr(user, "username", None),
        "password_hash": getattr(user, "password_hash", None),
        "latitude": getattr(user, "latitude", None),
        "longitude": getattr(user, "longitude", None),
        "type": getattr(user, "type", "normal"),
        "created_at": getattr(user, "created_at", None)
    }).execute()

    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return response.data

@router.get("/{user_id}")
def get_user(user_id: int):
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return response.data

@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    existing = supabase.table("users").select("*").eq("id", user_id).single().execute()
    if existing.error:
        raise HTTPException(status_code=500, detail=str(existing.error))
    if not existing.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    response = supabase.table("users").update({
        "name": user.name,
        "email": getattr(user, "email", None),
        "username": getattr(user, "username", None)
    }).eq("id", user_id).execute()

    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return {"message": "Usuário atualizado", "data": response.data}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    existing = supabase.table("users").select("*").eq("id", user_id).single().execute()
    if existing.error:
        raise HTTPException(status_code=500, detail=str(existing.error))
    if not existing.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    response = supabase.table("users").delete().eq("id", user_id).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=str(response.error))
    return {"message": "Usuário deletado"}


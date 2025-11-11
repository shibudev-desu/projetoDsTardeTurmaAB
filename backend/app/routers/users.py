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
def create_user(user: dict):

    new_user = {
        "id": len(fake_db["users"]) + 1,
        "email": user.get("email"),
        "username": user.get("username"),
        "name": user.get("name"),
        "password_hash": user.get("password_hash"),
        "latitude": user.get("latitude"),
        "longitude": user.get("longitude"),
        "type": user.get("type", "normal"),
        "created_at": user.get("created_at", "2025-01-01")
    }

    fake_db["users"].append(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: int):
    return next((u for u in fake_db["users"] if u["id"] == user_id), None)

@router.delete("/{user_id}")
def delete_user(user_id: int):
    index = next((i for i, u in enumerate(fake_db["users"]) if u["id"] == user_id), None)

    if index is None:
        return {"error": "User not found"}

    del fake_db["users"][index]
    return {"message": "User deleted"}

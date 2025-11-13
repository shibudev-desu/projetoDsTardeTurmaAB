from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]


@router.post("/")
def create_user(data: dict):
    # Evita duplicação de e-mails
    existing = supabase.table("users").select("*").eq("email", data.get("email")).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    response = supabase.table("users").insert(data).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="User not created")

    # Retorna o usuário criado (necessário pro teste)
    return response.data[0]


@router.put("/{user_id}")
def update_user(user_id: int, data: dict):
    response = supabase.table("users").update(data).eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]


@router.delete("/{user_id}")
def delete_user(user_id: int):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully", "id": user_id}

from fastapi import APIRouter
from app.db.fake_db import fake_db
from app.models import User

router = APIRouter()

@router.get("/")
def get_users():
    return fake_db["users"]

@router.post("/")
def create_user(user: User):
    new_user = {
        "id": len(fake_db["users"]) + 1,
        "name": user.name
    }
    fake_db["users"].append(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: int):
    user = next((u for u in fake_db["users"] if u["id"] == user_id), None)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    index = next((i for i, u in enumerate(fake_db["users"]) if u["id"] == user_id), None)
    if index is None:
        return None
    del fake_db["users"][index]
    return {"message": "User deleted"}

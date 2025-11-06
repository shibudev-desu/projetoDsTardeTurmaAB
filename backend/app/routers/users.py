"""
Rotas CRUD de usuários usando FastAPI com banco fake em memória.
"""

from fastapi import APIRouter
from app.models import User
from app.db.fake_db import fake_db

router = APIRouter()

# GET - Buscar todos usuários
@router.get("/")
def get_users():
    return fake_db['users']

# GET - Buscar usuário por ID
@router.get("/{user_id}")
def get_user(user_id: int):
    user = next((user for user in fake_db["users"] if user["id"] == user_id), None)

    if not user:
        return {"error": "User not found"}

    return user

# POST - Criar usuário
@router.post("/")
def create_user(user: User):
    new_user = {
        "id": len(fake_db['users']) + 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "bio": user.bio,
        "styles": user.styles
    }

    fake_db['users'].append(new_user)

    return new_user

# PUT - Atualizar usuário
@router.put("/{user_id}")
def update_user(user_id: int, user: User):

    # Procurar usuário pelo id real, não pela posição
    index = next((i for i, u in enumerate(fake_db['users']) if u["id"] == user_id), None)

    if index is None:
        return {"error": "User not found"}

    fake_db['users'][index] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "bio": user.bio,
        "styles": user.styles
    }

    return {"message": "User updated"}

# DELETE - Deletar usuário
@router.delete("/{user_id}")
def delete_user(user_id: int):

    index = next((i for i, u in enumerate(fake_db['users']) if u["id"] == user_id), None)

    if index is None:
        return {"error": "User not found"}

    del fake_db['users'][index]

    return {"message": "User deleted"}

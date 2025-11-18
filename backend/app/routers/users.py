"""
Este módulo define as rotas da API para operações relacionadas a usuários.
Ele permite buscar, criar, atualizar e deletar perfis de usuários.
"""
from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase

router = APIRouter()
supabase = get_supabase()


@router.get("/")
def get_users():
    """
    Retorna uma lista de todos os usuários.
    """
    response = supabase.table("users").select("*").execute()
    return response.data


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    """
    Retorna um usuário específico pelo seu ID.

    Args:
        user_id (int): O ID do usuário a ser retornado.

    Returns:
        dict: Os dados do usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado.
    """
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]


@router.post("/")
def create_user(data: dict):
    """
    Cria um novo usuário.

    Args:
        data (dict): Os dados do usuário a ser criado.

    Returns:
        dict: Os dados do usuário criado.

    Raises:
        HTTPException: Se o e-mail já estiver registrado ou se o usuário não puder ser criado.
    """
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

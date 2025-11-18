"""
Este módulo define as rotas da API para operações relacionadas a músicas.
Ele permite buscar, criar, atualizar e deletar músicas.
"""
from fastapi import APIRouter, HTTPException
from app.db.supabase_client import get_supabase

router = APIRouter()


@router.get("/")
def get_all_musics():
    """
    Retorna uma lista de todas as músicas.
    """
    supabase = get_supabase()
    try:
        response = supabase.table("musics").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{music_id}")
def get_music_by_id(music_id: int):
    """
    Retorna uma música específica pelo seu ID.

    Args:
        music_id (int): O ID da música a ser retornada.

    Returns:
        dict: Os dados da música.

    Raises:
        HTTPException: Se a música não for encontrada.
    """
    supabase = get_supabase()
    try:
        response = supabase.table("musics").select("*").eq("id", music_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Music not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_music(music: dict):
    """
    Cria uma nova música.

    Args:
        music (dict): Os dados da música a ser criada.

    Returns:
        dict: Os dados da música criada.
    """
    supabase = get_supabase()
    try:
        music_data = {
            "title": music.get("title"),
            "description": music.get("description"),
            "artist_id": music.get("artist_id"),
            "duration": music.get("duration"),
            "audio_url": music.get("audio_url"),  # ✅ Corrigido
            "posted_at": music.get("posted_at"),  # ✅ Corrigido
            "lyric": music.get("lyric"),
            "genre": music.get("genre"),
            "file_name": music.get("file_name"),
        }

        response = supabase.table("musics").insert(music_data).execute()
        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{music_id}")
def update_music(music_id: int, music: dict):
    """
    Atualiza uma música existente.

    Args:
        music_id (int): O ID da música a ser atualizada.
        music (dict): Os dados da música para atualização.

    Returns:
        dict: Os dados da música atualizada.

    Raises:
        HTTPException: Se a música não for encontrada.
    """
    supabase = get_supabase()
    try:
        response = supabase.table("musics").update(music).eq("id", music_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Music not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{music_id}")
def delete_music(music_id: int):
    """
    Deleta uma música existente pelo seu ID.

    Args:
        music_id (int): O ID da música a ser deletada.

    Returns:
        dict: Uma mensagem de sucesso.

    Raises:
        HTTPException: Se a música não for encontrada.
    """
    supabase = get_supabase()
    try:
        response = supabase.table("musics").delete().eq("id", music_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Music not found")
        return {"message": "Music deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Este módulo implementa um sistema de recomendação colaborativa baseado em usuários.
Ele encontra usuários com gostos musicais semelhantes e recomenda músicas que esses usuários gostaram,
mas que o usuário alvo ainda não ouviu.
"""
from typing import Dict, Any, List
from collections import defaultdict, Counter
from app.db.supabase_client import get_supabase
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/colab')
def recColab(
    user_id: int = None, 
    limit: int = 10, 
    neigh_limit: int = 200,
) -> List[Dict[str, Any]]:
    """
    Gera recomendações de música colaborativas para um usuário.

    Args:
        user_id (int): O ID do usuário para quem gerar recomendações.
        limit (int): O número máximo de recomendações a serem retornadas.
        neigh_limit (int): O número máximo de vizinhos (usuários semelhantes) a serem considerados.

    Returns:
        List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário representa uma música recomendada
                              com informações como ID, título, ID do artista e pontuação de similaridade.

    Raises:
        HTTPException: Se o usuário não for encontrado, não houver avaliações de música,
                       não houver candidatos para recomendação ou se o cálculo de Jaccard falhar.
    """
    try:
        supabase = get_supabase()

        if user_id is not None:
            user = supabase.table("users").select("id").eq("id", user_id).execute()
            if not user.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="User not found"
                )
        
        target_likes_q = supabase.table("user_music_ratings").select("music_id").eq("user_id", user_id).execute()
        target_likes = {r["music_id"] for r in (target_likes_q.data or [])}
        if not target_likes: raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Music Ratings not found ")
        
        ids_str = f"({','.join(map(str, target_likes))})"
        cdd_res = (
            supabase.table("user_music_ratings")
            .select("user_id")
            .filter("music_id", "in", ids_str)
            .eq("rating", 1)
            .neq("user_id", user_id)
            .execute()
        )
        user_counts = Counter(r["user_id"] for r in (cdd_res.data or []))
        cdd_uid = [uid for uid, _ in user_counts.most_common(neigh_limit)]
        
        if not cdd_uid: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Candidates not found."
            )
        
        likes_map = defaultdict(set)
        ids_str_users = f"({','.join(map(str, cdd_uid))})" if cdd_uid else "(0)"
        likes_res = (
            supabase.table("user_music_ratings")
            .select("user_id", "music_id")
            .filter("user_id", "in", ids_str_users)
            .eq("rating", 1)
            .execute()
        )
        for r in (likes_res.data or []):
            likes_map[r["user_id"]].add(r["music_id"])

        def jaccard(a:set, b:set):
            if not a and not b: return 0.0
            inter = len(a & b) 
            union = len(a | b)
            return (inter / union) if union else 0.0
        
        sim_scores = {}
        for uid, liked_set in likes_map.items():
            sim = jaccard(set(target_likes), liked_set)
            if sim > 0:
                sim_scores[uid] = sim
        if not sim_scores: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jaccard failed.")
           
        track_scores = Counter()
        for uid, sim in sim_scores.items():
            for mid in likes_map.get(uid, set()):
                if mid not in target_likes:
                    track_scores[mid] += sim

        if not track_scores: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracker failed.")
        
        top = track_scores.most_common(limit)
        music_ids = [m for m, _ in top]

        ids_str_music = f"({','.join(map(str, music_ids))})" if music_ids else "(0)"
        musics_q = supabase.table("musics").select("*").filter("id", "in", ids_str_music).execute()
        
        musics = []
        score_map = {m: s for m, s in top}
        for m in (musics_q.data or []):
            musics.append({
                "id": m["id"],
                "title": m.get("title"),
                "artist_id": m.get("artist_id"),
                "score": float(score_map.get(m["id"], 0.0))
            })
            
        musics.sort(key=lambda x: x["score"], reverse=True)
        return musics
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

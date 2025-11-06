from typing import Dict, Any, List
from app.db.supabase_client import get_supabase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/popular")
def recommend_popular(
    user_id: int, 
    limit: int = 10
) -> List[Dict[str, Any]]:
    supabase = get_supabase()

    if user_id is not None:
      user = supabase.table("users").select("id").eq("id", user_id).execute()
      if not user.data:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail="User not found"
          )

    user_rated = []
    rated = supabase.table("user_music_ratings").select("music_id").eq("user_id", user_id).execute()
    user_rated = [item["music_id"] for item in rated.data]
    ids_str = f"({','.join(map(str, user_rated))})"

    query = (
        supabase.table("musics")
        .select(
            "id",
            "title",
            "artist_id",
            "posted_at",
            "likes:user_music_ratings(count)"
        )
        .filter("id", "not.in", ids_str)
        .eq("likes.rating", "1")
        .order("posted_at", desc=True)
        .limit(limit)
    )
    result = query.execute()

    out = []
    for row in result.data:
        likes_count = row.get("likes", [{"count": 0}])[0]["count"]
        out.append({
            "id": row["id"],
            "title": row["title"],
            "artist_id": row["artist_id"],
            "likes": int(likes_count),
            "posted_at": row["posted_at"]
        })

    return out


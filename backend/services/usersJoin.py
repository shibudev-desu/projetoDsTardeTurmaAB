from typing import Dict, Any, List, Counter
from collections import defaultdict
from .popular import recommend_popular
from app.db.supabase_client import get_supabase
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get('colab')
def recColab(
    user_id: int = None, 
    limit: int = 10, 
    neigh_limit: int = 200,
) -> List[Dict[str, Any]]:
  supabase = get_supabase()

  if user_id is not None:
    user = supabase.table("users").select("id").eq("id", user_id).execute()
    if not user.data:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found"
        )
  
  target_likes_q = supabase.table("User_Music_Ratings").select("id").eq("user_id", user_id).execute()
  target_likes = {r.music_id for r in target_likes_q}
  if not target_likes: raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Music Ratings not found ")
  
  
  candidates_q = (UserMusicRating
                  .select(UserMusicRating.user, fn.COUNT(UserMusicRating.music).alias("common"))
                  .where((UserMusicRating.music.in_(list(target_likes))) & (UserMusicRating.rating == 1) & (UserMusicRating.user != user_id))
                  .group_by(UserMusicRating.user)
                  .order_by(fn.COUNT(UserMusicRating.music).desc())
                  .limit(neighbor_fetch_limit))
  '''
  SQL equivalente para mais clareza:
  SELECT user_id, COUNT(music_id) AS common
  FROM user_music_ratings
  WHERE music_id IN (:target_likes)  -- lista de IDs curtidos pelo usuário
    AND rating = 1
    AND user_id != :user_id
  GROUP BY user_id
  ORDER BY common DESC
  LIMIT :neighbor_fetch_limit;
  '''
  candidate_user_ids = [r.user_id for r in candidates_q]
  if not candidate_user_ids:
      return recommend_popular(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=user_id, limit=limit)
  
  likes_map = defaultdict(set)
  likes_q = (UserMusicRating
              .select(UserMusicRating.user, UserMusicRating.music)
              .where((UserMusicRating.user.in_(candidate_user_ids)) & (UserMusicRating.rating == 1)))
  for r in likes_q:
      likes_map[r.user_id].add(r.music_id)

  def jaccard(a:set, b:set):
    if not a and not b: return 0.0
    inter = len(a & b); union = len(a | b)
    return (inter / union) if union else 0.0
  
  sim_scores = {}
  # Calculo de similaridade
  for uid, liked_set in likes_map.items():
      sim = jaccard(set(target_likes), liked_set)
      if sim > 0:
          sim_scores[uid] = sim
  if not sim_scores:
      return recommend_popular(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=user_id, limit=limit)
  
  track_scores = Counter()
  for uid, sim in sim_scores.items():
      for mid in likes_map.get(uid, set()):
          if mid not in target_likes:
              track_scores[mid] += sim

  if not track_scores:
      return recommend_popular(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=user_id, limit=limit)
  
  top = track_scores.most_common(limit)
  music_ids = [m for m, _ in top]

  musics_q = Music.select().where(Music.id.in_(music_ids))
  musics = []
  score_map = {m: s for m, s in top}
  for m in musics_q:
      musics.append({
          "id": m.id,
          "title": getattr(m, "title", None),
          "artist_id": getattr(m, "artist_id", None),
          "score": float(score_map.get(m.id, 0.0))
      })
      
  musics.sort(key=lambda x: x["score"], reverse=True)
  return musics

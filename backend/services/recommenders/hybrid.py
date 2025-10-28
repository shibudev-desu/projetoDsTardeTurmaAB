# Traduzindo o código de peewee para ser utilizado com supabase.

from typing import List, Dict, Any
from collections import defaultdict
from utils.ramos_helper import try_import_models
from collab import recommend_collaborative_user_based
from ramos_popular import recommend_popular
from geo import recommend_geo
from app.db.supabase_client import get_supabase

def _normalize_score_map(m: dict) -> dict:
  if not m:
    return {}

  vals = list(m.values())
  mn = min(vals)
  mx = max(vals)

  if mx == mn:
    return {k: 1.0 for k in m}

  return {k: (v - mn) / (mx - mn) for k, v in m.items()}

async def recommend_hybrid(
  user_id: int,
  limit: int = 10,
  w_pop: float = 0.3,
  w_collab: float = 0.5,
  w_geo: float = 0.2,
  collab_similarity: str = "jaccard",
  geo_method: str = "haversine"
):
  supabase = get_supabase()

  pop = await recommend_popular(
    user_id=user_id,
    limit=limit * 3
  )

  try:
    coll = await recommend_collaborative_user_based(
      user_id=user_id,
      limit=limit * 3,
      similarity=collab_similarity
    )
  except Exception:
    coll = []

  geo = await recommend_geo(
    user_id=user_id,
    radius_km=20.0,
    limit=limit * 3,
    method=geo_method
  )

  # Aqui é feito a conversão para o score maps

  pop_map = {p["id"]: float(p.get("likes", 0.0)) for p in pop}
  coll_map = {c["id"]: float(c.get("score", 0.0)) for c in coll}
  geo_map = {
    g["id"]: (1.0 / (1.0 + g["distance_km"])) if g.get("distance_km") else 0.0
    for g in geo
  }

  pop_norm = _normalize_score_map(pop_map)
  coll_norm = _normalize_score_map(coll_map)
  geo_norm = _normalize_score_map(geo_map)
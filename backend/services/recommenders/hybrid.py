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
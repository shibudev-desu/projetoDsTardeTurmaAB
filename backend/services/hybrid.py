"""
Este módulo implementa um sistema de recomendação híbrido que combina diferentes abordagens
(popularidade, geolocalização) para fornecer recomendações de música mais abrangentes.
"""
# Traduzindo o código de peewee para ser utilizado com supabase.

from typing import List, Dict, Any
from collections import defaultdict
from utils.ramos_helper import try_import_models
from popular import recommend_popular
from geo import recommend_geo
from app.db.supabase_client import get_supabase

# Normalizando valores numéricos entre 0 e 1

def _normalize_score_map(m: dict) -> dict:
  """
  Normaliza os valores numéricos em um dicionário para uma escala de 0 a 1.

  Args:
      m (dict): Um dicionário onde as chaves são IDs e os valores são pontuações numéricas.

  Returns:
      dict: Um novo dicionário com as pontuações normalizadas.
  """
  if not m:
    return {}

  vals = list(m.values())
  mn, mx = min(vals), max(vals)

  if mx == mn:
    return {k: 1.0 for k in m}

  return {k: (v - mn) / (mx - mn) for k, v in m.items()}

async def recommend_hybrid(
  user_id: int,
  limit: int = 10,
  w_pop: float = 0.5,
  w_collab: float = 0.0, # desativado
  w_geo: float = 0.2,
  geo_method: str = "haversine"
):
  """
  Gera recomendações de música híbridas para um usuário, combinando popularidade e geolocalização.

  Args:
      user_id (int): O ID do usuário para quem as recomendações são geradas.
      limit (int): O número máximo de recomendações a serem retornadas.
      w_pop (float): Peso para as recomendações baseadas em popularidade.
      w_collab (float): Peso para as recomendações colaborativas (atualmente desativado).
      w_geo (float): Peso para as recomendações baseadas em geolocalização.
      geo_method (str): O método de cálculo de distância a ser usado para recomendações geográficas.

  Returns:
      List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário representa uma música recomendada
                            com informações como ID, título, ID do artista e pontuação híbrida.
  """
  supabase = get_supabase()

  # Recomendações individuais

  pop = await recommend_popular(
    user_id=user_id,
    limit=limit * 3
  )

  geo = await recommend_geo(
    user_id=user_id,
    radius_km=20.0,
    limit=limit * 3,
    method=geo_method
  )

  # Aqui é feito a conversão para o score maps

  pop_map = {p["id"]: float(p.get("likes", 0.0)) for p in pop}
  geo_map = {
    g["id"]: (1.0 / (1.0 + g["distance_km"])) if g.get("distance_km") else 0.0
    for g in geo
  }

  pop_norm = _normalize_score_map(pop_map)
  geo_norm = _normalize_score_map(geo_map)

  # Ajustes automáticos de pesos

  total = float(w_pop + w_geo) or 1.0
  w_pop /= total
  w_geo /= total

  combined = defaultdict(float)

  for mid, s in pop_norm.items():
    combined[mid] += w_pop * s
  for mid, s in geo_norm.items():
    combined[mid] += w_geo * s

  # Fallback em caso de ausência dos dados

  if not combined:
    return await recommend_popular(user_id=user_id, limit=limit)

  # Ordena e busca informações das músicas

  sorted_top = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:limit]
  ids = [i for i, _ in sorted_top]
  score_lookup = dict(sorted_top)

  # Busca das músicas no Supabase

  response = supabase.table("musics") \
    .select("id, title, artist_id") \
    .in_("id", ids) \
    .execute()

  musics = response.data or []

  # Insere o score final

  for m in musics:
    m["score"] = float(score_lookup.get(m["id"], 0.0))

  musics.sort(key=lambda x: x["score"], reverse=True)

  return musics
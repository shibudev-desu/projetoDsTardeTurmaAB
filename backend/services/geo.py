"""
Este módulo fornece funcionalidades para recomendar músicas com base na localização geográfica dos usuários e artistas.
Ele utiliza diferentes métodos de cálculo de distância, como Haversine e earth_distance, para encontrar músicas relevantes.
"""
from typing import List, Dict, Any, Tuple
from peewee import fn
import logging
from services.popular import recommend_popular
from utils.ramos_helper import try_import_models
import backend.utils.geo

logger = logging.getLogger(__name__)

def recommend_geo(User=None, Music=None, UserMusicRating=None, user_id: int = None, radius_km: float = 20.0, limit: int = 10, method: str = "haversine") -> List[Dict[str, Any]]:
  """
  Recomenda músicas com base na localização geográfica do usuário.

  Args:
      User: Modelo do usuário (Peewee).
      Music: Modelo da música (Peewee).
      UserMusicRating: Modelo de avaliação de música do usuário (Peewee).
      user_id (int): O ID do usuário para quem as recomendações são geradas.
      radius_km (float): O raio em quilômetros para buscar artistas próximos.
      limit (int): O número máximo de recomendações a serem retornadas.
      method (str): O método de cálculo de distância a ser usado ("haversine" ou "earth_distance").

  Returns:
      List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário representa uma música recomendada
                            com informações como ID, título, ID do artista, distância e data de postagem.

  Raises:
      RuntimeError: Se os modelos Peewee não forem fornecidos ou importados corretamente.
  """
  if not (User and Music and UserMusicRating):
    imported = try_import_models()
    User = User or imported.get("User")
    Music = Music or imported.get("Music")
    UserMusicRating = UserMusicRating or imported.get("UserMusicRating")

  if not (User and Music and UserMusicRating):
    raise RuntimeError("Models not provided.")

  user = User.get_or_none(User.id == user_id)

  if not user or getattr(user, "latitude", None) is None or getattr(user, "longitude", None) is None:
    return recommend_popular(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=user_id, limit=limit)

  q_limit = 1000

  rated_subq = (
    UserMusicRating
      .select(UserMusicRating.music)
      .where(UserMusicRating.user == user_id)
  )

  out = []

  if method == "haversine":
    # Directly execute haversine logic if method is explicitly set to haversine
    pass # The haversine logic is below this block
  elif method == "earth_distance":
    try:
      meter_limit = int(radius_km * 1000.0)
      q = (
        Music
          .select(Music, fn.earth_distance(fn.ll_to_earth(User.latitude, User.longitude), fn.ll_to_earth(user.latitude, user.longitude)).alias("dist_m"))
          .join(User, on=(Music.artist == User.id))
          .where((fn.earth_distance(fn.ll_to_earth(User.latitude, User.longitude), fn.ll_to_earth(user.latitude, user.longitude)) < meter_limit) & (Music.id.not_in(rated_subq)))
          .order_by(fn.earth_distance(fn.ll_to_earth(User.latitude, User.longitude), fn.ll_to_earth(user.latitude, user.longitude)), Music.posted_at.desc())
          .limit(limit)
      )
      
      for row in q:
        dist_m = getattr(row, "dist_m", None)
        out.append({
          "id": row.id,
          "title": getattr(row, "title", None),
          "artist_id": getattr(row, "artist_id", None),
          "distance_km": (float(dist_m) / 1000.0) if dist_m is not None else None,
          "posted_at": getattr(row, "posted_at", None)
        })

    except Exception as exc:
      logger.warning("earth_distance approach failed (%s). Falling back to haversine.", exc)
      method = "haversine" # Fallback to haversine if earth_distance fails
  
  if method == "haversine" and not out: # Only run haversine if earth_distance didn't already provide results or failed
    sample_q = (
      Music
        .select(Music, User.latitude, User.longitude)
        .join(User, on=(Music.artist == User.id))
        .where((User.latitude.is_null(False)) & (User.longitude.is_null(False)) & (Music.id.not_in(rated_subq)))
        .order_by(Music.posted_at.desc())
        .limit(q_limit)
    )

    candidates: List[Tuple[float, Any]] = []
    seen = set()
    
    for row in sample_q:
      if row.id in seen:
        continue
      
      try:
        dist_km = backend.utils.geo._haversine_km(float(user.latitude), float(user.longitude), float(row.latitude), float(row.longitude))
      except Exception:
        continue
      
      if dist_km <= float(radius_km):
        candidates.append((dist_km, row))
        seen.add(row.id)

    candidates.sort(key=lambda x: (x[0],))
    
    for dist_km, row in candidates[:limit]:
      out.append({
        "id": row.id,
        "title": getattr(row, "title", None),
        "artist_id": getattr(row, "artist_id", None),
        "distance_km": float(dist_km),
        "posted_at": getattr(row, "posted_at", None)
      })

  if len(out) < limit:
    more = recommend_popular(user_id=user_id, limit=limit - len(out))
    existing = {x["id"] for x in out}
    
    for m in more:
      if m["id"] not in existing:
        out.append(m)

  return out
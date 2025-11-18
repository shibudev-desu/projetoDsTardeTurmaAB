"""
Este módulo contém a implementação da fórmula de Haversine para calcular a distância
entre dois pontos geográficos (latitude e longitude) na superfície da Terra.
"""
import math

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
  """
  Calcula a distância Haversine entre dois pontos geográficos em quilômetros.

  Args:
      lat1 (float): Latitude do primeiro ponto.
      lon1 (float): Longitude do primeiro ponto.
      lat2 (float): Latitude do segundo ponto.
      lon2 (float): Longitude do segundo ponto.

  Returns:
      float: A distância Haversine entre os dois pontos em quilômetros.

  Raises:
      ValueError: Se as coordenadas fornecidas forem inválidas ou não numéricas.
  """
  if lat1 is None or lat2 is None or lon1 is None or lon2 is None:
    raise ValueError("Coordenadas inválidas para haversine")
  
  try:
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
  except ValueError:
    raise ValueError("Coordenadas não numéricas para haversine")
  
  r = 6371.0
  a = math.sin(dlat/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlon/2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  
  return r * c
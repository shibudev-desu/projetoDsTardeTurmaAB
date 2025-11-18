"""
Este módulo contém funções utilitárias para cálculos geográficos, como a distância Haversine.
"""
import math

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância Haversine entre dois pontos geográficos em quilômetros.

    Args:
        lat1 (float): Latitude do primeiro ponto.
        lon1 (float): Longitude do primeiro ponto.
        lat2 (float): Latitude do segundo ponto.
        lon2 (float): Longitude do segundo ponto.

    Returns:
        float: A distância Haversine entre os dois pontos em quilômetros.
    """
    R = 6371  # Radius of Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

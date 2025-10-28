import supabase as sb
from haversine import haversine

url = "https://mflpegvqdnqdfvbvfdos.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbHBlZ3ZxZG5xZGZ2YnZmZG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNDQ3ODEsImV4cCI6MjA3NTYyMDc4MX0.DLcfAc8u1dA91oISnOEMTIq1GxQZ7AAUXWiWmlf0Uo4"

def recommendGeo(user, limit=10, radius=10):
  try:
    client = sb.create_client(url, key)
  except Exception as e:
    print(f"Connection:\n{e}")
    return
  
  try:
    rawMusics = client.table("musics").select("title, artist_id").limit(limit).execute()
  except Exception as e:
    print(f"Musics:\n{e}")
    return
  
  res = rawMusics.data
  userIds = []

  for m in res:
    if m['artist_id'] not in userIds:
      userIds.append(m['artist_id'])

  coordinates = []

  try:
    for id in userIds:
      rawIds = client.table("users").select("latitude, longitude").eq("id", id).execute()
      coordinates.append(rawIds.data[0])
  except Exception as e:
    print(f"Users:\n{e}")
    return

  default = coordinates[0]
  distances = []

  for coordinate in coordinates:
    print(coordinate)
    distances.append(haversine(default["longitude"], default["latitude"], coordinate["longitude"], coordinate["latitude"]))

if __name__ == "__main__":
  recommendGeo(1, 4,)
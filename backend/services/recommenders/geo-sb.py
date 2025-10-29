import supabase as sb
from haversine import haversine

url = "https://mflpegvqdnqdfvbvfdos.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbHBlZ3ZxZG5xZGZ2YnZmZG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNDQ3ODEsImV4cCI6MjA3NTYyMDc4MX0.DLcfAc8u1dA91oISnOEMTIq1GxQZ7AAUXWiWmlf0Uo4"

def recommendGeo(user, limit=10, radius=10):
  try:
    client = sb.create_client(url, key)
  except Exception as e:
    print(f"Init connection:\n{e}")
    return
  
  try:
    rawMusics = client.table("musics").select("title, artist_id").limit(limit).execute()
  except Exception as e:
    print(f"Select musics:\n{e}")
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
    print(f"Select locations:\n{e}")
    return

  default = coordinates[0]
  distances = {}
  index = 0

  for coordinate in coordinates:
    distances[userIds[index]] = haversine(default["longitude"], default["latitude"], coordinate["longitude"], coordinate["latitude"])
    index += 1
  
  del index
  del distances[user]

  # for i in list(distances.keys()):
  #   if distances[i] > radius:
  #     del distances[i]
  
  idsSearch = list(distances.keys())
  
  try:
    rawSelectRated = client.table("user_music_ratings").select("music_id").eq("user_id", user).execute()
  except Exception as e:
    print(f"Select rated musics:\n{e}")
    return
  
  idsExcludedMusic = []

  for i in rawSelectRated.data:
    idsExcludedMusic.append(i["id"])

  try:
    rawMusics = client.table("musics").select("id").in_("artist_id", idsSearch).not_.in_("id", idsExcludedMusic).execute()
  except Exception as e:
    print(f"Select musics nearby:\n{e}")
    return
  
  idMusics = []

  for i in rawMusics.data:
    idMusics.append(i["id"])

  try:
    lastQuery = client.table("musics").select("id, title, artist_id(name)").in_("id", idMusics).execute()
  except Exception as e:
    print(f"Last query:\n{e}")
    return

  return lastQuery.data

if __name__ == "__main__":
  recommendGeo(1, 4)
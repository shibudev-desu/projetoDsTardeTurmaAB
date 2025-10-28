import supabase as sb

url = "https://mflpegvqdnqdfvbvfdos.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbHBlZ3ZxZG5xZGZ2YnZmZG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNDQ3ODEsImV4cCI6MjA3NTYyMDc4MX0.DLcfAc8u1dA91oISnOEMTIq1GxQZ7AAUXWiWmlf0Uo4"

def recommendGeo(user, limit=10):
  try:
    client = sb.create_client(url, key)
  except Exception as e:
    print(e)
  
  try:
    raw = client.table("musics").select("title, artist_id").limit(limit).execute()
  except Exception as e:
    print(e)
  
  res = raw.data
  userIds = []

  for m in res:
    print(f"artist_id: {m['artist_id']}")
    userIds.append(m['artist_id'])

  print(userIds)
  

if __name__ == "__main__":
  recommendGeo(1, 2)
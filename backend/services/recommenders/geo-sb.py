import supabase as sb

url = "https://mflpegvqdnqdfvbvfdos.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbHBlZ3ZxZG5xZGZ2YnZmZG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNDQ3ODEsImV4cCI6MjA3NTYyMDc4MX0.DLcfAc8u1dA91oISnOEMTIq1GxQZ7AAUXWiWmlf0Uo4"

def recommendGeo(user):
  try:
    client = sb.create_client(url, key)
  except Exception as e:
    print(e)
  
  raw = client.table("musics").select("title, artist_id(name)").execute()
  print(raw.data)

if __name__ == "__main__":
  recommendGeo(1)
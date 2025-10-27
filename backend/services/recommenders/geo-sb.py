import supabase as sb

url = "https://mflpegvqdnqdfvbvfdos.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbHBlZ3ZxZG5xZGZ2YnZmZG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNDQ3ODEsImV4cCI6MjA3NTYyMDc4MX0.DLcfAc8u1dA91oISnOEMTIq1GxQZ7AAUXWiWmlf0Uo4"
table = "users"

def showData():
  try:
    client = sb.create_client(url, key)
    response = client.table(table).select("*").execute()
    dados_clientes = response.data
    
    if not dados_clientes:
      print(f"[{table}] is empty or doesn't exist.")
    else:
      for registro in dados_clientes:
        print(registro)

  except Exception as e:
    print(f"Detalhes do erro: {e}")

if __name__ == "__main__":
  showData()
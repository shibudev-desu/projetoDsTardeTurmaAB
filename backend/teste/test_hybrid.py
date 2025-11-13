import asyncio
from app.db.supabase_client import get_supabase
from services.hybrid import hybrid

async def main():
  supabase = get_supabase()
  print("Conexão Supabase ativa")

  user_id = 1

  print("Gerando recomendações para o usuário", user_id)
  result = await hybrid(user_id=user_id, limit=5)

  print("\n--- Recomendações ---")
  for m in result:
    print(f"{m['id']} - {m.get('title', 'Sem título')} (score: {m['score']:.3f})")

if __name__ == "__main__":
  asyncio.run(main())
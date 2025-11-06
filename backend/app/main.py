from fastapi import FastAPI
from app.routers import users, music, artists, popular
from app.db.supabase_client import get_supabase, SUPABASE_KEY, SUPABASE_URL

app = FastAPI(title="Backend React Native API")

# incluir rotas
app.include_router(users, prefix="/api/users", tags=["users"])
app.include_router(artists, prefix="/api/artists", tags=["artists"])
app.include_router(music, prefix="/api/music", tags=["music"])
app.include_router(popular, prefix="/api/popular", tags=["popular"])

@app.get("/")
def root():
    return {"message": "Backend ativo 🚀"}

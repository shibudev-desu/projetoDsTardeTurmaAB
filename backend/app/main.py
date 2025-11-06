from fastapi import FastAPI
from app.routers import users, music
from services import popular
from app.db.supabase_client import get_supabase, SUPABASE_KEY, SUPABASE_URL
app = FastAPI(title="Backend React Native API")

# incluir rotas
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(music.router, prefix="/api/music", tags=["music"])
app.include_router(popular.router, prefix="/api", tags=["popular"])

@app.get("/")
def root():
    return {"message": "Backend ativo 🚀"}

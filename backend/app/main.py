from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.music import router as music_router
from app.routers.artists import router as artists_router
from app.routers.styles import router as styles_router
from services.popular import router as popular_router
from app.db.supabase_client import get_supabase, SUPABASE_KEY, SUPABASE_URL

app = FastAPI(title="Backend React Native API")

# incluir rotas
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(artists_router, prefix="/api/artists", tags=["artists"])
app.include_router(music_router, prefix="/api/music", tags=["music"])
app.include_router(popular_router, prefix="/api/popular", tags=["popular"])

@app.get("/")
def root():
    return {"message": "Backend ativo 🚀"}

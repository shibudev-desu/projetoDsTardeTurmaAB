from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers import users, music
from app.routers.artists import router as artists_router
from app.routers.music import router as music_router  
from services import popular, usersJoin
from app.db.supabase_client import get_supabase, SUPABASE_KEY, SUPABASE_URL

app = FastAPI(title="Backend React Native API")

# incluir rotas
# TODO: Essa duas rotas estão dando problema, elas devem existir ou podem ser excluídas?
# app.include_router(users.router, prefix="/api/users", tags=["users"])
# app.include_router(music.router, prefix="/api/music", tags=["music"])

app.include_router(music_router, prefix="", tags=["MusicsRoot"])
app.include_router(artists_router, prefix="/api/artists", tags=["Artists"])
app.include_router(popular.router, prefix="/api", tags=["popular"])
app.include_router(usersJoin.router, prefix="/api", tags=["colab"])

@app.get("/")
def root():
    return {}

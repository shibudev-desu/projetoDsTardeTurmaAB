"""
Este módulo é o ponto de entrada principal para a aplicação FastAPI.
Ele configura a aplicação, inclui os roteadores para usuários, músicas e artistas,
e define a rota raiz.
"""
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.music import router as music_router
from app.routers.artists import router as artists_router
from services import popular, usersJoin
from app.db.supabase_client import get_supabase, SUPABASE_KEY, SUPABASE_URL

app = FastAPI(title="Backend React Native API")

# incluir rotas
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(music_router, prefix="/api/musics", tags=["music"])

app.include_router(artists_router, prefix="/api/artists", tags=["Artists"])
app.include_router(popular.router, prefix="/api", tags=["popular"])
app.include_router(usersJoin.router, prefix="/api", tags=["colab"])

@app.get("/")
def root():
    """
    Retorna uma resposta vazia para a rota raiz da API.
    """
    return {}

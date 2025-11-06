from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.artists import router as artists_router
from app.routers.music import router as music_router

app = FastAPI()

app.include_router(users_router, prefix="/api/users")
app.include_router(artists_router, prefix="/api/artists")
app.include_router(music_router, prefix="/api/musics")

@app.get("/")
def root():
    return {}

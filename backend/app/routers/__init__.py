from .users import router as users_router
from .music import router as music_router
from .artists import router as artists_router
from services.popular import router as popular_router

users = users_router
music = music_router
artists = artists_router
popular = popular_router

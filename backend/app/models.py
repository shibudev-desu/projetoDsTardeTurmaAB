from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    name: str

class Artist(BaseModel):
    name: str

class Music(BaseModel):
    title: str
    description: str | None = None
    artist_id: int | None = None
    duration: str | None = None
    posted_at: str | None = None

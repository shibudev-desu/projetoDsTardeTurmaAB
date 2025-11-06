from pydantic import BaseModel

class User(BaseModel):
    name: str

class Artist(BaseModel):
    name: str

class Music(BaseModel):
    title: str
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    lyrics: str # snippet from UI
    genre: str
    title: str = None


class GenerateResponse(BaseModel):
    song_url: str
    local_path: str
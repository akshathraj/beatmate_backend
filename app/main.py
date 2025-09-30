from fastapi import FastAPI
from app.api import router

app = FastAPI(title="BeatMate Backend")
app.include_router(router, prefix="/api")
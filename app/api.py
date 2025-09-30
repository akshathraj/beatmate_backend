from fastapi import APIRouter, HTTPException, Request
from app.models import GenerateRequest, GenerateResponse
from app.services import lyrics_service, song_service

router = APIRouter()

# Step 1 + 2: Generate song request (async)
@router.post('/generate-song', response_model=GenerateResponse)
def generate_song(req: GenerateRequest):
    try:
        # Complete lyrics
        complete_lyrics = lyrics_service.generate_complete_lyrics(req.lyrics, req.genre)

        # Generate song (async task)
        music_task = song_service.generate_song_from_lyrics(
            complete_lyrics, req.genre, title=req.title
        )

        # Return task info
        return GenerateResponse(
            song_url=f"MusicGPT task_id: {music_task['task_id']}",
            local_path=f"Conversion IDs: {music_task['conversion_id_1']}, {music_task['conversion_id_2']}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Step 3: Webhook endpoint to receive final mp3/audio
@router.post('/webhook/musicgpt')
async def musicgpt_webhook(request: Request):
    """
    MusicGPT calls this webhook with final song info.
    Saves the mp3 locally.
    """
    payload = await request.json()
    print("=== MusicGPT Webhook Received ===")
    print(payload)

    try:
        conversion_path = payload.get("conversion_path")
        title = payload.get("title", "song")

        if conversion_path:
            import requests
            from .utils import storage

            r = requests.get(conversion_path)
            audio_bytes = r.content
            filename = storage.timestamped_filename(title, "mp3")
            local_path = storage.local_save_file(audio_bytes, filename)

            print(f"Saved song locally: {local_path}")
        return {"success": True}

    except Exception as e:
        print(f"Webhook processing error: {e}")
        return {"success": False, "error": str(e)}
from google import genai
from app import config

# Initialize Gemini client once
# client = genai.Client(api_key="AIzaSyCVox8noLLQQOgokVscwkaMmQ4t6F7r-DA")
client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_complete_lyrics(lyrics_snippet: str, genre: str) -> str:
    """
    Calls Gemini API to generate completed lyrics.
    """
    prompt_text = f"""
Generate a complete song lyrics based on the following snippet.
Format the lyrics using [Intro], [Verse], [Chorus], [Bridge], [Outro] tags.
Separate lines with newline characters (\\n). Do not include extra metadata.
Genre: {genre}
Lyrics snippet:
{lyrics_snippet}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text
    )

    # Get the generated lyrics text
    lyrics = response.text.strip()

     # Debug log
    print("=== Gemini Generated Lyrics ===")
    print(lyrics)

    return lyrics
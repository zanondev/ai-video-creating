from auth_settings import api_keys
import requests

VOICE_ID = "bIHbv24MWmeRgasZH58o"  
ELEVENLABS_API_KEY = api_keys.ELEVENLABS_API_KEY
OUTPUT_PATH = 'audio_output.mp3'
CHUNK_SIZE = 1024  

def generate_voiceover(narration_text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
    "Accept": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY,
    }
    data = {
        "text": narration_text.content,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
    }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.ok:
        with open(OUTPUT_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                 if chunk:
                    f.write(chunk)
    print("Audio stream saved successfully.")


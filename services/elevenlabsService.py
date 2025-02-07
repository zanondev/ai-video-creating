from settings import api_keys
import requests

VOICE_ID = "bIHbv24MWmeRgasZH58o"  
ELEVENLABS_API_KEY = api_keys.ELEVENLABS_API_KEY
OUTPUT_PATH = 'audio_output.mp3'
CHUNK_SIZE = 1024  

def generate_voiceover(index, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
    "Accept": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY,
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
        "stability": 0.5, # Controls the emotional range and consistency of the voice. (Low (e.g. 0.3): More variation and emotion; High (e.g. 0.8): More stable, monotone voice)
        "similarity_boost": 0.8, # Controls how closely the AI matches the original voice. (Low (e.g. 0.3): Less similar to original; High (e.g. 0.8): More similar, may replicate artifacts)
        "style": 0.0, # Style: Enhances the speaker's style (value range 0-100) (Low (e.g. 20): Subtle style enhancement; High (e.g. 80): Strong style enhancement, may affect stability)
        "use_speaker_boost": True # Speaker Boost: Increases likeness to original speaker (boolean) (false: Normal voice, true: Increased similarity, useful for weaker voices)
        }
        
    }
    response = requests.post(url, json=data, headers=headers)
    if response.ok:
        with open(f"{index}.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                 if chunk:
                    f.write(chunk)
    print("Audio stream saved successfully.")

    return response.ok


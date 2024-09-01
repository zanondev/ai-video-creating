import openai
from auth_settings import api_keys

openai.api_key = api_keys.OPENAI_API_KEY

def generate_narration(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]
    )
    return response.choices[0].message

def generate_image(prompt, size="1024x1024"):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    return response.data[0].url
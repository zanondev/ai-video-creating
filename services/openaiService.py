import openai
from settings import api_keys

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

"""
Gera imagem a partir de um prompt de texto.

Args:
    prompt (str): texto para geração da imagem
    size (str): dimensão da imagem.

Returns:
    str: url da imagem criada.
"""
def generate_image(prompt, size='1792x1024'):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    return response.data[0].url
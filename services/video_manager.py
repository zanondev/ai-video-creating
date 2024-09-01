from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import requests
import os
from services import elevenlabs_service

def create_video(image_urls, audio_path=elevenlabs_service.OUTPUT_PATH, video_output_path='output_video.mp4'):
    # Carregar o áudio e calcular a duração total
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    
    # Calcular a duração de cada imagem com base no total de imagens
    image_duration = total_duration / len(image_urls)
    
    clips = []
    image_paths = []  # Para rastrear os arquivos de imagem baixados
    
    # Criar clipes de imagem com a duração calculada
    for i, image_url in enumerate(image_urls):
        image_response = requests.get(image_url)
        image_path = f'temp_image_{i}.png'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        image_paths.append(image_path)
        
        image_clip = ImageClip(image_path).set_duration(image_duration)
        clips.append(image_clip)
    
    # Concatenar clipes de imagem e adicionar o áudio
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio_clip)
    
    # Salvar o vídeo
    video.write_videofile(video_output_path, fps=24)
    print(f"Video stream saved successfully: {video_output_path}")

    # Apagar os arquivos de áudio e imagem temporários
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    for image_path in image_paths:
        if os.path.exists(image_path):
            os.remove(image_path)

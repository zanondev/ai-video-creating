from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips
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


def create_video2(mediaObject, index):
    audioClip = AudioFileClip(mediaObject["audio"])
    
    # Baixar a imagem e salvá-la temporariamente
    imageResponse = requests.get(mediaObject["image"])
    imagePath = f"temp_image_{index}.png"
    
    with open(imagePath, 'wb') as f:
        f.write(imageResponse.content)
    
    # Criar um clipe de imagem com a duração do áudio
    imageClip = ImageClip(imagePath).set_duration(audioClip.duration)
    
    # Adicionar o áudio ao clipe de imagem
    video = imageClip.set_audio(audioClip)
    
    # Definir o caminho de saída do vídeo
    videoOutputPath = f"{index}.mp4"
    
    # Salvar o vídeo
    video.write_videofile(videoOutputPath, fps=24)
    print(f"Video stream saved successfully: {videoOutputPath}")
    
    # Apagar o arquivo de imagem temporário
    if os.path.exists(imagePath):
        os.remove(imagePath)
    
    # Retornar o caminho do vídeo gerado
    return videoOutputPath

def mergeVideo(videoPaths, outputPath="merged_output.mp4"):
    # Carregar todos os clipes de vídeo na ordem fornecida
    clips = [VideoFileClip(video) for video in videoPaths]
    
    # Concatenar todos os clipes
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Escrever o vídeo resultante para o caminho de saída
    final_video.write_videofile(outputPath, fps=24)
    print(f"Merged video saved successfully: {outputPath}")
    
    # Fechar os clipes para liberar memória
    for clip in clips:
        clip.close()
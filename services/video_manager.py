from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, vfx, concatenate_videoclips, CompositeVideoClip, concatenate_audioclips
import requests
import os
import openai
from pysrt import SubRipFile, SubRipItem, SubRipTime
import moviepy.editor as mp
from auth_settings import api_keys

openai.api_key = api_keys.OPENAI_API_KEY

def transcribe_audio_to_subtitles(audio, video, language="pt"):
    # Extraindo áudio do vídeo
    # Transcrevendo o áudio com a nova API OpenAI
    with open(audio, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            language=language,
            temperature=0,
            response_format="json"
        )

    transcription = response["text"]
    segments = response["segments"]  # Timestamps e texto

    # Criando um arquivo de legendas (.srt)
    subs = SubRipFile()
    for i, segment in enumerate(segments):
        start_time = SubRipTime.from_ordinal(int(segment["start"] * 1000))
        end_time = SubRipTime.from_ordinal(int(segment["end"] * 1000))
        subtitle = SubRipItem(i + 1, start=start_time, end=end_time, text=segment["text"])
        subs.append(subtitle)

    subs_file_path = "output_subtitles.srt"
    subs.save(subs_file_path, encoding="utf-8")
    return subs_file_path, transcription


def add_subtitles_to_video(mp4_file_path, srt_file_path, output_file_path="final_video_with_subtitles.mp4"):
    video = mp.VideoFileClip(mp4_file_path)

    # Carregar legendas em um arquivo de texto legível
    with open(srt_file_path, "r", encoding="utf-8") as f:
        subtitles = f.read()

    # Adicionando legendas ao vídeo
    subtitle_clip = mp.TextClip(subtitles, fontsize=24, color="white", bg_color="black", method="caption", size=video.size)
    subtitle_clip = subtitle_clip.set_duration(video.duration)
    
    # Combinar vídeo e legendas
    final_video = mp.CompositeVideoClip([video, subtitle_clip])
    final_video.write_videofile(output_file_path, codec="libx264", audio_codec="aac")

    return output_file_path


def process_video_with_subtitles(audio, video, language="en"):
    srt_file_path, transcription = transcribe_audio_to_subtitles(audio, language)
    final_video_path = add_subtitles_to_video(video, srt_file_path)
    print(f"Vídeo final com legendas: {final_video_path}")
    print(f"Transcrição: {transcription}")

def add_audio_to_video(mp3_path, mp4_path, output_path="final_video.mp4"):
    try:
        # Carregar o vídeo e o áudio
        video_clip = VideoFileClip(mp4_path)
        audio_clip = AudioFileClip(mp3_path)
        
        # Ajustar a duração do áudio para a do vídeo (se áudio for maior que vídeo)
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        else:
            # Repetir o áudio até cobrir a duração do vídeo, se necessário
            audio_clip = audio_clip.fx(vfx.loop, duration=video_clip.duration)
        
        # Definir o áudio do vídeo
        video_clip_with_audio = video_clip.set_audio(audio_clip)
        
        # Escrever o vídeo com o áudio no arquivo de saída
        video_clip_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Fechar os clipes para liberar memória
        video_clip.close()
        audio_clip.close()
        
        # Retornar o caminho do arquivo final
        return output_path
    
    except Exception as e:
        print(f"Erro ao adicionar áudio ao vídeo: {e}")
        return None

def create_image_video(mediaObject, index):
    # Caminhos de saída para os arquivos temporários e final
    temp_video_path = f"temp_video_{index}.mp4"
    final_video_path = f"{index}.mp4"
    
    try:
        # 1) Carregar o áudio e obter sua duração
        audioClip = AudioFileClip(mediaObject["audio"])
        audio_duration = audioClip.duration  # A duração do áudio vai definir a duração do vídeo

        # 2) Baixar a imagem da URL
        imageResponse = requests.get(mediaObject["image"])
        image_path = f"temp_image_{index}.png"
        with open(image_path, 'wb') as f:
            f.write(imageResponse.content)

        # Criar um clipe de vídeo da imagem com a duração do áudio
        imageClip = ImageClip(image_path).set_duration(audio_duration)

        # Aplicar fade in/out no vídeo (imagem)
        videoClip = imageClip.fadein(1).fadeout(1)  # 1 segundo de fade in/out

        # Salvar o vídeo temporário (sem áudio)
        videoClip.write_videofile(temp_video_path, fps=24, codec="libx264")
        videoClip.close()

        # 3) Renomear o vídeo final
        os.rename(temp_video_path, final_video_path)

        # Retornar o nome do arquivo final
        return final_video_path

    except Exception as e:
        print(f"Erro ao criar o vídeo: {e}")
        return None

def CreateVideo(mediaObject, index):
    # Caminhos de saída para os arquivos temporários e final
    temp_video_path = f"temp_video_{index}.mp4"
    temp_video_with_audio_path = f"temp_video_with_audio_{index}.mp4"
    final_video_path = f"{index}.mp4"
    
    try:
        # 1) Carregar o áudio e obter sua duração
        audioClip = AudioFileClip(mediaObject["audio"])
        audio_duration = audioClip.duration

        # 2) Baixar a imagem da URL
        imageResponse = requests.get(mediaObject["image"])
        image_path = f"temp_image_{index}.png"
        with open(image_path, 'wb') as f:
            f.write(imageResponse.content)

        # Criar um clipe de vídeo da imagem com duração do áudio
        imageClip = ImageClip(image_path).set_duration(audio_duration)

        # Aplicar fade in/out no vídeo (imagem)
        videoClip = imageClip.fadein(1).fadeout(1)  # 1 segundo de fade in/out

        # Salvar o vídeo temporário sem áudio
        videoClip.write_videofile(temp_video_path, fps=24, codec="libx264")
        videoClip.close()

        # 3) Combinar o vídeo com o áudio
        video_with_audio = CompositeVideoClip([VideoFileClip(temp_video_path).set_audio(audioClip)])
        video_with_audio.write_videofile(temp_video_with_audio_path, fps=24, codec="libx264", audio_codec="aac")
        video_with_audio.close()

        # 4) Renomear o vídeo final
        os.rename(temp_video_with_audio_path, final_video_path)

        # Retornar o nome do arquivo final
        return final_video_path

    finally:
        # 5) Apagar arquivos temporários
        for temp_file in [temp_video_path, image_path, temp_video_with_audio_path]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def merge_videos(videoPaths, outputPath="video_merged_output.mp4"):
    try:
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
        
        # Retornar o caminho do arquivo final
        return outputPath

    except Exception as e:
        print(f"Erro ao mesclar os vídeos: {e}")
        return None

def merge_audio(audioPaths, outputPath="audio_merged_output.mp3"):
    try:
        # Carregar todos os arquivos de áudio
        audio_clips = [AudioFileClip(audio) for audio in audioPaths]
        
        # Concatenar todos os clipes de áudio
        final_audio = concatenate_audioclips(audio_clips)
        
        # Escrever o áudio concatenado para o caminho de saída
        final_audio.write_audiofile(outputPath)
        print(f"Merged audio saved successfully: {outputPath}")
        
        # Retornar o caminho do arquivo final
        return outputPath

    except Exception as e:
        print(f"Erro ao mesclar os áudios: {e}")
        return None

# def create_video(image_urls, audio_path=elevenlabs_service.OUTPUT_PATH, video_output_path='output_video.mp4'):
#     # Carregar o áudio e calcular a duração total
#     audio_clip = AudioFileClip(audio_path)
#     total_duration = audio_clip.duration
    
#     # Calcular a duração de cada imagem com base no total de imagens
#     image_duration = total_duration / len(image_urls)
    
#     clips = []
#     image_paths = []  # Para rastrear os arquivos de imagem baixados
    
#     # Criar clipes de imagem com a duração calculada
#     for i, image_url in enumerate(image_urls):
#         image_response = requests.get(image_url)
#         image_path = f'temp_image_{i}.png'
#         with open(image_path, 'wb') as f:
#             f.write(image_response.content)
#         image_paths.append(image_path)
        
#         image_clip = ImageClip(image_path).set_duration(image_duration)
#         clips.append(image_clip)
    
#     # Concatenar clipes de imagem e adicionar o áudio
#     video = concatenate_videoclips(clips, method="compose")
#     video = video.set_audio(audio_clip)
    
#     # Salvar o vídeo
#     video.write_videofile(video_output_path, fps=24)
#     print(f"Video stream saved successfully: {video_output_path}")

#     # Apagar os arquivos de áudio e imagem temporários
#     if os.path.exists(audio_path):
#         os.remove(audio_path)
    
#     for image_path in image_paths:
#         if os.path.exists(image_path):
#             os.remove(image_path)


# def create_video2(mediaObject, index, fade_duration=1):
#     """
#     Cria um vídeo com imagem e áudio, aplicando fade in e fade out apenas no vídeo (imagem).
    
#     :param mediaObject: Dicionário contendo 'audio' (URL do áudio) e 'image' (URL da imagem).
#     :param index: Índice para nomear o arquivo de saída.
#     :param fade_duration: Duração do fade in/out em segundos (somente visual).
#     :return: Caminho do arquivo de vídeo gerado.
#     """
#     # Carregar o áudio
#     audioClip = AudioFileClip(mediaObject["audio"])
    
#     # Baixar a imagem e salvá-la temporariamente
#     imageResponse = requests.get(mediaObject["image"])
#     imagePath = f"temp_image_{index}.png"
    
#     with open(imagePath, 'wb') as f:
#         f.write(imageResponse.content)
    
#     # Criar um clipe de imagem com a duração do áudio
#     imageClip = ImageClip(imagePath).set_duration(audioClip.duration)
    
#     # Adicionar o áudio ao clipe de imagem
#     video = imageClip.set_audio(audioClip)
    
#     # Aplicar fade in e fade out apenas no vídeo (imagem)
#     video = video.fadein(fade_duration).fadeout(fade_duration)

#     # Definir o caminho de saída do vídeo
#     videoOutputPath = f"{index}.mp4"
    
#     # Salvar o vídeo com parâmetros específicos para codec e áudio
#     video.write_videofile(
#         videoOutputPath,
#         fps=24,
#         codec="libx264",
#         audio_codec="aac",
#         temp_audiofile="temp-audio.m4a",
#         remove_temp=True
#     )
#     print(f"Video stream saved successfully: {videoOutputPath}")
    
#     # Apagar o arquivo de imagem temporário
#     if os.path.exists(imagePath):
#         os.remove(imagePath)
    
#     # Retornar o caminho do vídeo gerado
#     return videoOutputPath




# from moviepy.editor import VideoFileClip, concatenate_videoclips

# def mergeVideoWithTransition(videoPaths, outputPath="merged_output.mp4", fade_duration=3):
#     # Lista para armazenar os clipes processados
#     clips = []
    
#     for i, video in enumerate(videoPaths):
#         clip = VideoFileClip(video)
        
#         # Se não for o primeiro clipe, ajusta a transição
#         if i > 0:
#             # Transição suave no vídeo (dissolve) mantendo o áudio contínuo
#             clip = clip.crossfadein(fade_duration)
        
#         clips.append(clip)

#     # Combina todos os clipes em sequência
#     final_video = concatenate_videoclips(clips, method="compose")

#     # Escrever o vídeo resultante
#     final_video.write_videofile(outputPath, fps=24, audio_codec="aac")
#     print(f"Merged video saved successfully: {outputPath}")

#     # Fechar os clipes para liberar memória
#     for clip in clips:
#         clip.close()

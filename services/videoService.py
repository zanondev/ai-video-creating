from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, vfx, concatenate_videoclips, concatenate_audioclips
import requests
import os
import openai
from settings import api_keys

openai.api_key = api_keys.OPENAI_API_KEY

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
        image_path = f"{index}.png"
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
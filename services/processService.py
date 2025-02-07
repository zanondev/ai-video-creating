import os
from services import elevenlabsService, textService, openaiService, videoService, tempService

def process_text(text: list[str], fullText: str, rootPath: str):
    audioFiles = []
    imageVideosFiles = []
    tempFiles = []

    for index, text in enumerate(text):
        # gera arquivo de audio com a narração do trecho de texto e adiciona o caminho do produto em uma lista
        elevenlabsService.generate_voiceover(index, text)
        audioFiles.append(f"{index}.mp3")

        # Adiciona ao prompt de especificação para geração de imagem
        text = textService.text_image_especification(text, fullText)

        # Gera url da imagem do trecho de texto
        imageUrl = openaiService.generate_image(text)

        # cria aquivo .mp4 com a imagem do loop
        imageVideoOutputPath = videoService.create_image_video({
        'audio': f"{index}.mp3",  
        'image': imageUrl         
        }, index)

        # adiciona caminho do arquivo .mp4 em uma lista 
        imageVideosFiles.append(imageVideoOutputPath)

        # Cria lista de arquivos temporarios a serem apagados
        tempFiles.append({
        'audio': f"{index}.mp3",  
        'image': f"{index}.png",
        'video': f"{index}.mp4"      
        })

    # Realiza merge das midias criando produto final
    mergedAudio = videoService.merge_audio(audioFiles)
    mergedImagesVideo = videoService.merge_videos(imageVideosFiles)

    # Junta os merges resultando no produto final
    videoService.add_audio_to_video(mergedAudio, mergedImagesVideo)

    # Exclui arquivos .mp3 e .mp4 temporarios
    tempService.exclude_temp_media(rootPath, tempFiles, [mergedAudio, mergedImagesVideo])

        


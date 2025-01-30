from services import openai_service, elevenlabs_service, video_manager
from prompts import prompt_service
import re
import os

def splitPrompt(prompt):
    result = openai_service.generate_narration(prompt)
    return [re.sub(r'^\d+\.\s*', '', item.strip()) for item in result.content.split('\n') if item]

def setNarrationText():
    textTheme = input("Theme of the text (ex. Technology, The History of Art): ") or "Uma curiosidade sobre o monstro do lago ness"
    objective = input("Objective of the text (ex. Educate, Entertain, Inspire, Inform): ") or "Educate"
    emotion = input("Desired emotion of the text (ex. Curiosity, Motivation): ") or "Curiosity"
    narrationStyle = input("Narration style (ex: Formal, Casual, Humorous, Serious): ") or "Casual"
    language = input("Language (ex. English, Spanish, Portuguese): ") or "Portugues - BR"
    lenght = input("Length of the Script (Ex: Short, Medium, Long): ") or "Short"

    userPromptNarration = prompt_service.get_narration_prompt(textTheme, objective, emotion, narrationStyle, language, lenght)

    createdNarrationText = openai_service.generate_narration(userPromptNarration)
    print("Narration text generated")
    return createdNarrationText

def setAudio(index, text):
    return elevenlabs_service.generate_voiceover(index, text)

def cleanTempMidias(midias):
    for media_path in midias:
        if os.path.exists(media_path["audio"]):
            os.remove(media_path["audio"])
            print(f"Deleted: {media_path["audio"]}")
        else:
            print(f"File not found: {media_path["audio"]}")

def cleanTempVideos(videos):
    for video_path in videos:
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Deleted: {video_path}")
        else:
            print(f"File not found: {video_path}")

def main():
    # createdNarrationText = setNarrationText()
    
    # splitedNarrationPromptToCreate = prompt_service.get_divided_narration_prompt(createdNarrationText)
    
    # splitedNarration = splitPrompt(splitedNarrationPromptToCreate)
    
    # videos = []
    # midias = []
    # imageVideos = []
    
    # for index, text in enumerate(splitedNarration):
    #     # gerar audio
    #     response = setAudio(index, text)
    #     if response:
    #         print("Narration voice file generated")
    #     else:
    #         print("Error generating narration voice file")
    #         return
        
    #     text = text + ' Special condition for the image generation: Please ensure that the image does not include any text, writing, or numbers in any form.'
    #     # gerar imagem 
    #     imageUrl = openai_service.generate_image(text)

    #     mediaObject = {
    #     'audio': f"{index}.mp3",  
    #     'image': imageUrl         
    #     }
    #     midias.append(mediaObject)

    #     # criar midia 
    #     imageVideoOutputPath = video_manager.create_image_video(mediaObject, index)
    #     imageVideos = [].append(imageVideoOutputPath)
    
    # videosTeste = ['0.mp4', '1.mp4', '2.mp4', '3.mp4', '4.mp4', '5.mp4']
    # audioTeste = ['0.mp3', '1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3']
    # # fazer merge das midias criando produto final
   
    # mergedAudio = video_manager.merge_audio(audioTeste)
    # mergedImagesVideo = video_manager.merge_videos(videosTeste)

    # finalVideo = video_manager.add_audio_to_video(mergedAudio, mergedImagesVideo)
    video_manager.process_video_with_subtitles("audio_merged_output.mp3", "final_video.mp4")


    
if __name__ == "__main__":
    main()
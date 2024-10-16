from services import openai_service, elevenlabs_service, video_manager
from prompts import prompt_service
import re

def splitPrompt(prompt):
    result = openai_service.generate_narration(prompt)
    return [re.sub(r'^\d+\.\s*', '', item.strip()) for item in result.content.split('\n') if item]

def setNarrationText():
    textTheme = input("Theme of the text (ex. Technology, The History of Art): ")
    objective = input("Objective of the text (ex. Educate, Entertain, Inspire, Inform) : ")
    emotion = input("Desired emotion of the text (ex. Curiosity, Motivation): ")
    narrationStyle = input("Narration style (ex: Formal, Casual, Humorous, Serious): ")
    language = input("Language (ex. English, Spanish, Portuguese): ")
    lenght = input("Length of the Script (Ex: Short, Medium, Long): ")

    userPromptNarration = prompt_service.get_narration_prompt(textTheme, objective, emotion, narrationStyle, language, lenght)

    createdNarrationText = openai_service.generate_narration(userPromptNarration)
    print("Narration text generated")
    return createdNarrationText

def setAudio(createdNarrationText):
    elevenlabs_service.generate_voiceover(createdNarrationText)
    print("Narration voice file generated")

def setImages(createdNarrationText):
    imagePromptToCreate = prompt_service.get_images_prompt(createdNarrationText)
    
    imageDescriptions = splitPrompt(imagePromptToCreate)
    imageUrlList = []

    for i, prompt in enumerate(imageDescriptions):
        url = openai_service.generate_image(prompt)
        imageUrlList.append(url)
    
    print("Images descriptions generated")
    return imageUrlList

def divideNarration(createdNarrationText):
    splitedNarrationPromptToCreate = prompt_service.get_divided_narration_prompt(createdNarrationText)
    
    splitedNarration = splitPrompt(splitedNarrationPromptToCreate)

    for i, prompt in enumerate(splitedNarration):
        url = openai_service.generate_image(prompt)

# def cleanSplitedNarration(splitedNarration):
#     # Nova lista para armazenar as partes válidas (sem **)
#     clean_narration = []
    
#     # Percorre cada item da lista e verifica se contém "**"
#     for i, prompt in enumerate(splitedNarration):
#         if '**' not in prompt:  # Verifica se não há metadados como **Tema** ou **Estilo**
#             clean_narration.append(prompt)  # Adiciona apenas as partes válidas
    
#     return clean_narration

def setVideo(imageUrlList):
    video_manager.create_video(imageUrlList)

def main():
    createdNarrationText = setNarrationText()
    divideNarration(createdNarrationText);


    # setAudio(createdNarrationText)

    imageUrlList = setImages(createdNarrationText)

    setVideo(imageUrlList)
    
if __name__ == "__main__":
    main()
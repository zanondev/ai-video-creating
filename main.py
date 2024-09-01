from services import openai_service, elevenlabs_service, video_manager
from prompts import prompt_service
import re

def generate_image_descriptions(imagePromptToCreate):
    imagePromptCreated = openai_service.generate_narration(imagePromptToCreate)
    return  [re.sub(r'^\d+\.\s*', '', item.strip()) for item in imagePromptCreated.content.split('\n') if item]

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
    
    imageDescriptions = generate_image_descriptions(imagePromptToCreate)
    imageUrlList = []

    for i, prompt in enumerate(imageDescriptions):
        url = openai_service.generate_image(prompt)
        imageUrlList.append(url)
    
    print("Images descriptions generated")
    return imageUrlList

def setVideo(imageUrlList):
    video_manager.create_video(imageUrlList)

def main():
    createdNarrationText = setNarrationText()

    setAudio(createdNarrationText)

    imageUrlList = setImages(createdNarrationText)

    setVideo(imageUrlList)
    
if __name__ == "__main__":
    main()
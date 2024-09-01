from services import openai_service, elevenlabs_service, video_manager
import re

def generate_image_descriptions(imagePromptToCreate):
    imagePromptCreated = openai_service.generate_narration(imagePromptToCreate)
    return  [re.sub(r'^\d+\.\s*', '', item.strip()) for item in imagePromptCreated.content.split('\n') if item]

def main():
    # Gerar narração
    userPromptNarration = input("Digite o texto para a narração: ")
    createdNarration = openai_service.generate_narration(userPromptNarration)
    print("Narration text generated")

    # Gerar audio da narração
    elevenlabs_service.generate_voiceover(createdNarration)
    print("Narration voice file generated")

    # Gerar imagens
    imagePromptToCreate = f"""
                                Based on the following text: 
                                "{createdNarration}"

                                Generate a list of image descriptions to illustrate the content strictly in the following format:

                                1. Description 1
                                2. Description 2
                                3. Description 3

                                Do not include introductions, explanations, or additional text. Ensure that the descriptions are created in English.
                                """
    
    imageDescriptions = generate_image_descriptions(imagePromptToCreate)
    imageUrlList = []

    for i, prompt in enumerate(imageDescriptions):
        url = openai_service.generate_image(prompt)
        imageUrlList.append(url)
        print(f"Image {i+1} URL:", url)

    # Criar video
    # image_url_1 = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-Mp2mJBuQsrbnxQCyUy5miAN8/user-7fbqn21GZix40dLzWgz6oFAq/img-7rDmXdfNc08BFC5bUYFRjafx.png?st=2024-08-31T19%3A40%3A37Z&se=2024-08-31T21%3A40%3A37Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-08-31T01%3A48%3A42Z&ske=2024-09-01T01%3A48%3A42Z&sks=b&skv=2024-08-04&sig=tqqEHjignnMMSHHt3AzTcPVXEKWZ2K9hZ%2BfXcYxGfRs%3D'

    video_manager.create_video(imageUrlList)

if __name__ == "__main__":
    main()
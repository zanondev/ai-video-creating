from services import openaiService
import re

def get_splited_text(text):
    return f"""
    Based on the following text: "{text}"
    Please divide this text into sections that can be transformed into images. Each section should correspond to a specific part of the text that can be visualized as an image. Return the original text divided into parts that represent these sections.
    The format should be:
    1. Text section 1
    2. Text section 2
    3. Text section 3
    Do not include descriptions or additional text. Ensure the output follows the order of the original text, and when combined, they should represent the entire text exactly as it was.
    """

def split_prompt(prompt):
    result = openaiService.generate_narration(prompt)
    return [re.sub(r'^\d+\.\s*', '', item.strip()) for item in result.content.split('\n') if item]

def text_image_especification(text: str, fullText):
     return 'Possuo um contexto que é o seguinte: ' + fullText + ' Agora, crie uma imagem para o seguinte trecho: ' + text + ' Certifique-se que a imagem não tenha nenhum tipo de texto, numerção ou qualquer tipo de escrita. Isso é muito importante.'
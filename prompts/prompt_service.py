def get_narration_prompt(theme, 
                         objective='Educate', 
                         emotion='Curiosity', 
                         narrationStyle='Casual', 
                         language='Portugues - BR', 
                         lenght='Short'):
    return f"""
            Create text on the theme {theme}. The objective of this text is {objective},
            and it should evoke the emotion of {emotion} in the readers.
            The text style should be {narrationStyle}, and it should be written in {language}.
            Make the lenght ot the text {lenght}.
            """

def get_images_prompt(createdNarration):
    return f"""
                                Based on the following text: "{createdNarration}"
                                Generate a list of image descriptions to illustrate the content strictly in the following format:
                                1. Description 1
                                2. Description 2
                                3. Description 3
                                Do not include introductions, explanations, or additional text. Ensure that the descriptions are created in English.
                                Add a note to each description: "Ensure to not generate text in the image."
                                """
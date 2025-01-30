def get_divided_narration_prompt(createdNarration):
    return f"""
    Based on the following text: "{createdNarration}"
    Please divide this text into sections that can be transformed into images. Each section should correspond to a specific part of the text that can be visualized as an image. Return the original text divided into parts that represent these sections.
    The format should be:
    1. Text section 1
    2. Text section 2
    3. Text section 3
    Do not include descriptions or additional text. Ensure the output follows the order of the original text, and when combined, they should represent the entire text exactly as it was.
    """

def get_narration_prompt(theme, 
                         objective, 
                         emotion, 
                         narrationStyle, 
                         language, 
                         length):
    return f"""
            Create text on the theme "{theme}". The objective of this text is "{objective}",
            and it should evoke the emotion of "{emotion}" in the readers.
            The text style should be "{narrationStyle}", and it should be written in "{language}".
            Make the length of the text "{length}".
            Important: Do not include any metadata, such as **Title**, **Subtitle**, **Theme**, or **Style**. Only generate the text itself, without introductions, headings, or any other extra elements. The result should be a continuous, flowing narrative.
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
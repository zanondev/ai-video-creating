import os

def create_temp_folder():
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def export_text(lines: list):
    temp_dir = create_temp_folder()

    file_path = os.path.join(temp_dir, 'text.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        for index, line in enumerate(lines):
            file.write(f"{index} = {line}\n")
    
    print(f"Text generated succefully. Path: {file_path}")

def export_image_url(url: str):
    temp_dir = create_temp_folder()
    file_path = os.path.join(temp_dir, 'images.txt')
    
    with open(file_path, 'a', encoding='utf-8') as file: 
        file.write(url + ';\n\n')
    
    print(f"Image URL added successfully. Path: {file_path}")

def exclude_temp_media(root_path, tempFiles, mergedFiles):
    print(f"Removing temp files...")
    for temp_file in tempFiles:
        audio_file = temp_file.get('audio')
        image_file = temp_file.get('image')
        video_file = temp_file.get('video')

        for file_name in [audio_file, image_file, video_file]:
            if file_name:
                file_path = os.path.join(root_path, file_name)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting {file_name}: {e}")

    for merged_file in mergedFiles:
        merged_file_path = os.path.join(root_path, merged_file)
        if os.path.exists(merged_file_path):
            try:
                os.remove(merged_file_path)
            except Exception as e:
                print(f"Error deleting {merged_file}: {e}")
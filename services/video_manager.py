from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import requests

def create_video(image_url, audio_path, video_output_path):
    image_response = requests.get(image_url)
    image_path = 'temp_image.png'
    with open(image_path, 'wb') as f:
        f.write(image_response.content)
    
    image_clip = ImageClip(image_path).set_duration(AudioFileClip(audio_path).duration)
    audio_clip = AudioFileClip(audio_path)
    video = image_clip.set_audio(audio_clip)
    video.write_videofile(video_output_path, fps=24)
    print(f"Vídeo criado com sucesso: {video_output_path}")
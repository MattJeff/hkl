import moviepy.editor as mp

def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

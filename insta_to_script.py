import instaloader
import os
import subprocess
import logging
import time
import moviepy.editor as mp
from pathlib import Path

# Téléchargement de la vidéo depuis Instagram
def download_instagram_video(post_url, download_folder):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, post_url.split('/')[-2])
    L.download_post(post, target=download_folder)
    return post

# Extraction de l'audio de la vidéo
def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

# Transcription de l'audio avec l'API OpenAI
def transcribe_audio_with_openai(audio_path, openai_api_key):
    command = f'curl https://api.openai.com/v1/audio/transcriptions ' \
              f'-H "Authorization: Bearer {openai_api_key}" ' \
              f'-H "Content-Type: multipart/form-data" ' \
              f'-F file="@{audio_path}" ' \
              f'-F model="whisper-1"'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        logging.error("Error in transcription request: %s", result.stderr)
        raise Exception(f"Transcription request failed: {result.stderr}")

    transcription = result.stdout
    return transcription

def main():
    # Entrée de l'URL via le terminal
    post_url = input("Entrez l'URL de la vidéo Instagram: ")

    # Variables
    download_folder = 'downloads'  # Dossier où la vidéo sera téléchargée
    audio_filename = 'audio.wav'
    transcription_filename = 'transcription.txt'

    # Créez le dossier de téléchargement s'il n'existe pas
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Téléchargement de la vidéo
    print("Téléchargement de la vidéo...")
    post = download_instagram_video(post_url, download_folder)

    # Trouver le fichier vidéo téléchargé
    video_path = None
    for file in os.listdir(download_folder):
        if file.endswith(".mp4"):
            video_path = os.path.join(download_folder, file)
            break

    if video_path is None:
        print("Erreur : Impossible de trouver la vidéo téléchargée.")
        return

    # Extraction de l'audio
    print("Extraction de l'audio...")
    audio_path = os.path.join(download_folder, audio_filename)
    extract_audio(video_path, audio_path)

    # Transcription de l'audio
    print("Transcription de l'audio...")
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    transcription = transcribe_audio_with_openai(audio_path, openai_api_key)

    # Sauvegarde de la transcription
    transcription_path = os.path.join(download_folder, transcription_filename)
    with open(transcription_path, 'w') as f:
        f.write(transcription)

    print("Vidéo téléchargée et transcrite avec succès.")

if __name__ == "__main__":
    main()

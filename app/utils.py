import os

def find_video_path(download_folder):
    for file in os.listdir(download_folder):
        if file.endswith(".mp4"):
            return os.path.join(download_folder, file)
    raise Exception("Erreur : Impossible de trouver la vidéo téléchargée.")

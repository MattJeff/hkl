import subprocess
import logging

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

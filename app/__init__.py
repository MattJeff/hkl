from flask import Flask

def create_app():
    app = Flask(__name__)

    from .download import download_instagram_video
    from .extract import extract_audio
    from .transcribe import transcribe_audio_with_openai

    @app.route('/')
    def home():
        return "L'application est fonctionnelle."

    @app.route('/process', methods=['POST'])
    def process():
        data = request.json
        post_url = data.get('post_url')
        openai_api_key = data.get('openai_api_key')

        try:
            post = download_instagram_video(post_url, 'downloads')
            video_path = find_video_path('downloads')
            audio_path = extract_audio(video_path, 'downloads/audio.wav')
            transcription = transcribe_audio_with_openai(audio_path, openai_api_key)

            username, profile = get_instagram_profile_info(post)

            return {
                'text': transcription,
                'url': post.url,
                'comments': post.comments,
                'likes': post.likes,
                'download_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'creator': username,
                'creator_info': {
                    'followers': profile.followers,
                    'followees': profile.followees,
                    'mediacount': profile.mediacount
                }
            }
        except Exception as e:
            return {'error': str(e)}, 500

    return app

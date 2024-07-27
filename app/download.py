import instaloader

def download_instagram_video(post_url, download_folder):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, post_url.split('/')[-2])
    L.download_post(post, target=download_folder)
    return post

import os
import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'remote_components': 'ejs:github',
        'js_runtimes': {'node': {}},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if 'requested_downloads' in info and info['requested_downloads']:
            filepath = info['requested_downloads'][0].get('filepath')
        else:
            filepath = ydl.prepare_filename(info)

    return filepath if filepath and os.path.exists(filepath) else None
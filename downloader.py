import os
import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'js_runtimes': ['node'],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("video") and (file.endswith(".mp4") or file.endswith(".webm")):
            return file

    return None
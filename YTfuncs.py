import os
import asyncio
from yt_dlp import YoutubeDL

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}


def extract_song_url(link: str) -> str:
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(link, download=False)
        url_sound = info['formats'][0]['url']
    return url_sound





if __name__ == "__main__":
    print(extract_song_url("https://youtu.be/DtL_giO-EB8"))

from youtubesearchpython.__future__ import VideosSearch
import urllib.parse
from urllib import *
import asyncio
import youtubesearchpython
from yt_dlp import YoutubeDL

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}


class VideoDiscord:
    def __init__(self, name: str, link: str, description: str):
        self.name = name
        self.link = link
        self.description = description

    def get_name(self):
        return self.name

    def get_link(self):
        return self.link

    def get_description(self):
        return self.description


def extract_song_url(link: str) -> str:
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(link, download=False)
        url_sound = info['formats'][0]['url']
    return url_sound


async def get_videos_list(query: str, size: int = 3) -> list:
    """Get list of VideoDiscord class"""
    idx = 1
    result = []
    videos_search = VideosSearch(query, limit=size)
    while idx <= size:
        video_result = await videos_search.next()
        video_info = video_result['result']
        video_info = video_info[0]
        video = VideoDiscord(video_info['title'], video_info['link'], video_info['title'])
        result.append(video)
        idx += 1
    return result


if __name__ == "__main__":

    results = asyncio.run(get_videos_list("Police"))
    print(results)

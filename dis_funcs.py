import discord
from asyncio import sleep
from urllib.parse import urlparse
import YTfuncs

FFMPEG_SOURCE = "FFmpeg/FFmpeg.exe"
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


def get_italic(string: str) -> str:
    return "*{0}*".format(string)


def get_bold(string: str) -> str:
    return "**{0}**".format(string)


def get_underline(string: str) -> str:
    return "__{0}__".format(string)


def get_strikethrough(string: str) -> str:
    return "~~{0}~~".format(string)


def get_code_block(string: str) -> str:
    return "`{0}`".format(string)


async def run_music(vc, link):
    if vc.is_playing():
        vc.stop()
    if urlparse(link).scheme:
        audio_link: str = YTfuncs.extract_song_url(link)
        vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_SOURCE, source=audio_link, **FFMPEG_OPTIONS))
    while vc.is_playing():  # because of AFK
        await sleep(60)
    if not vc.is_paused():
        await vc.disconnect(force=False)

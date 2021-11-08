import dotenv
from dotenv import load_dotenv
from asyncio import sleep
import os
import discord
import validators
import dis_format
import quotesAPI
import nasa
import YTfuncs

client = discord.Client()
load_dotenv()
prefix = os.environ['prefix']
global vc

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
FFMPEG_SOURCE = os.environ['ffmpeg_source'] + 'ffmpeg.exe'


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print(f"Prefix is - {prefix}")


@client.event
async def on_message(message):
    # Ignoring self messages
    if message.author == client.user:
        return

    # Hello response
    if message.content.startswith(prefix + 'hello'):
        await message.channel.send('Hello!')

    # Random quote from ZenQuotes
    if message.content.startswith(prefix + 'inspire'):
        await message.channel.send(quotesAPI.get_quote())

    # Celestial of the day from NASA API
    if message.content.startswith(prefix + 'celestial'):
        result: nasa.Celestial = nasa.get_celestial_of_the_day()

        await message.channel.send("**" + result.get_name() + "**")
        await message.channel.send("Description - ||" + result.get_description() + "||")
        await message.channel.send(result.get_picture())

    # Changes command prefix
    if message.content.startswith(prefix + 'prefix'):
        result_prefix = message.content.replace((prefix + 'prefix '), '')
        if len(result_prefix) > 1:
            message.channel.send("Incorrect prefix")
        else:
            globals()['prefix'] = result_prefix
            dotenv.set_key(".env", 'prefix', result_prefix)
            await message.channel.send("Prefix changed to {0}".format(result_prefix))
            print(f"Prefix changed to {result_prefix}")

    # Music Player
    if message.content.startswith(prefix + 'play'):
        link = message.content.replace((prefix + 'play '), '')
        global vc
        try:
            voice_channel: discord.channel.VoiceChannel = message.author.voice.channel
            vc = await voice_channel.connect()
        except Exception as e:
            print("ERROR " + f" {e}")
        if vc.is_playing:
            vc.stop()
        if validators.url(link):
            audio_link: str = YTfuncs.extract_song_url(link)
            vc.play(discord.FFmpegPCMAudio(executable=FFMPEG_SOURCE, source=audio_link, **FFMPEG_OPTIONS))
        while vc.is_playing():  # because of AFK
            await sleep(60)
        if not vc.is_paused():
            await vc.disconnect(force=False)


if __name__ == "__main__":
    client.run(os.environ["TOKEN"])

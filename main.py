import dotenv
from dotenv import load_dotenv
from asyncio import sleep
from discord.ext import commands
import os
import discord
import asyncio
from urllib.parse import urlparse
import dis_funcs
import quotesAPI
import nasa
import YTfuncs

load_dotenv()
prefix = os.environ['prefix']
client = commands.Bot(command_prefix=prefix)
client.case_insensitive = False
discord.opus.load_opus(r"Opus\opus.dll")
submit_wait: bool = False
video_results = []
video_query = []
global vc


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
FFMPEG_SOURCE = os.environ['ffmpeg_source'] + 'ffmpeg.exe'


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print(f"Prefix is - {client.command_prefix}")


#########################################       COMMANDS        ########################################################

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')


@client.command()
async def celestial(ctx):
    result: nasa.Celestial = nasa.get_celestial_of_the_day()
    await ctx.send("**" + result.get_name() + "**")
    await ctx.send(result.get_description())
    await ctx.channel.send(result.get_picture())


@client.command()
async def inspire(ctx):
    await ctx.send(quotesAPI.get_quote())


@client.command()
async def prefix(ctx, arg):
    result_prefix = arg
    if len(result_prefix) > 1:
        ctx.send("Incorrect prefix")
    else:
        globals()['prefix'] = result_prefix
        dotenv.set_key(".env", 'prefix', result_prefix)
        client.command_prefix = result_prefix
        await ctx.send("Prefix changed to {0}".format(result_prefix))
        print(f"Prefix changed to {result_prefix}")


@client.command()
async def play(ctx, *, arg):
    link: str = ""
    global vc
    try:
        voice_channel: discord.channel.VoiceChannel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except Exception as e:
        print("ERROR -" + f" {e}")
    global video_results

    if urlparse(arg).scheme:
        link = arg
    elif str.isdigit(arg):
        idx = int(arg)
        if idx > len(video_results):
            await ctx.send("Invalid number")
            return
        else:
            selected_video: YTfuncs.VideoDiscord = video_results[idx]
            link = selected_video.get_link()
    else:
        if video_results is None:
            return
        else:
            video_results = await YTfuncs.get_videos_list(arg)
            idx = 0
            print(len(video_results))
            while idx < len(video_results):
                await ctx.send("{0}. {1}\n".format(dis_funcs.get_bold(str(idx + 1)), video_results[idx].get_name()))
                idx += 1
            return

    await dis_funcs.run_music(vc, link)

#########################################       COMMANDS        ########################################################


if __name__ == "__main__":
    client.run(os.environ["TOKEN"])

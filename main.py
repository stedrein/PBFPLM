import dotenv
from dotenv import load_dotenv
import os
import discord
import common
import nasa

client = discord.Client()
load_dotenv()
prefix = os.environ['prefix']


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
# Ignoring self messages
async def on_message(message):
    if message.author == client.user:
        return

    # Hello response
    if message.content.startswith(prefix + 'hello'):
        await message.channel.send('Hello!')

    # Random quote from ZenQuotes
    if message.content.startswith(prefix + 'inspire'):
        await message.channel.send(common.get_quote())

    # Celestial of the day from NASA API
    if message.content.startswith(prefix + 'celestial'):
        result: nasa.Celestial = nasa.get_celestial_of_the_day()

        await message.channel.send(result.get_name())
        await message.channel.send(result.get_description())
        await message.channel.send(result.get_picture())

    if message.content.startswith(prefix + 'prefix'):
        dotenv.set_key()

client.run(os.environ["TOKEN"])

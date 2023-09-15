import logging
import discord
from discord.ext import commands
import os
from preprocessor import preprocess_text
from voicevox import Voicevox
from textToSpeechQueue import Text2SpeechQueue, SpeakTask

counter = 0

description = '''
voicevoxの読み上げbot
'''
host = os.environ.get("VOICEVOX_HOST", "127.0.0.1")
port = os.environ.get("VOICEVOX_PORT", "50021")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("$"),
    description=description,
    intents=intents,
)

voicevox = Voicevox(host, int(port))
voice_queue = Text2SpeechQueue(bot, voicevox)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.listen()
async def on_message(message:discord.Message):
    if (
        type(message.channel) is discord.channel.VoiceChannel
        and bot.user in message.channel.members
        and message.author != bot.user
        and not message.content.startswith('$')
        and message.guild
        and type(message.guild.voice_client) is discord.VoiceClient
        and message.guild.voice_client.is_connected()
    ):
        buf = await voicevox.genarete_sound(text=preprocess_text(message.content))
        if buf is None:
            await message.reply('audio failed')
            return

        src = discord.FFmpegOpusAudio(
            source=buf,
            pipe=True
        )
        voice_queue.add(SpeakTask(
            message=message,
            source=src
        ))
import logging
import discord
from discord.ext import commands
import aiohttp
import aiofiles
import os
import json
from preprocessor import preprocess_text
from io import BytesIO

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.listen()
async def on_message(message:discord.Message):
    if type(message.channel) is discord.channel.VoiceChannel:
        members = message.channel.members
        if (
            bot.user in members
            and message.author != bot.user
            and not message.content.startswith('$')
            and message.guild
            and type(message.guild.voice_client) is discord.VoiceClient
        ):
            buf =  await genarete_sound(text=preprocess_text(message.content), host=host, port=port)
            if buf:
                source = discord.FFmpegOpusAudio(source=buf, pipe=True)
                message.guild.voice_client.play(source)
            else:
                await message.channel.send('audio failed')

async def genarete_sound(text, speaker=1, host='localhost', port='50021', speed='100', pitch='0') -> BytesIO | None:
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{host}:{port}/audio_query', params=params, timeout=30) as query_res:
                if query_res.status != 200:
                    return None
                headers = {'Content-Type': 'application/json'}
                query_json = await query_res.json()
                query_json["outputSamplingRate"] = 24000
                query_json["speedScale"] = int(speed) / 100
                query_json["pitchScale"] = int(pitch) / 100
            async with session.post(f'http://{host}:{port}/synthesis', headers=headers, params=params, data=json.dumps(query_json), timeout=30) as response:
                if response.status != 200:
                    return None
                try:
                    return BytesIO(await response.read())
                except Exception as e:
                    print(f'error in synthesis : {e}')
                    return None
    except Exception as e:
        print(f'error in session: {e}')
        return None
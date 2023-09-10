import discord
from discord.ext import commands
import aiohttp
import aiofiles
import os
import json

counter = 0

description = '''
voicevoxの読み上げbot
'''

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
async def on_message(message:discord.message):
    channel_type = type(message.channel)
    if channel_type is discord.channel.VoiceChannel:
        members = message.channel.members
        if bot.user in members and message.author != bot.user and not message.content.startswith('$'):
            filename =  await text_to_wav(text=message.content)
            if filename != "Failed":
                source = await discord.FFmpegOpusAudio.from_probe(source=filename)
                message.guild.voice_client.play(source)
            else:
                await message.channel.send('audio failed')

async def genarete_wav(text, speaker=1, filepath='./audio.wav', host='localhost', port='50021', speed='100', pitch='0'):
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{host}:{port}/audio_query', params=params, timeout=30) as query_res:
                if query_res.status != 200:
                    return False
                headers = {'Content-Type': 'application/json'}
                query_json = await query_res.json()
                query_json["outputSamplingRate"] = 24000
                query_json["speedScale"] = int(speed) / 100
                query_json["pitchScale"] = int(pitch) / 100
            async with session.post(f'http://{host}:{port}/synthesis', headers=headers, params=params, data=json.dumps(query_json), timeout=30) as response:
                if response.status != 200:
                    return False
                try:
                    async with aiofiles.open(os.path.dirname(os.path.abspath(__file__)) + '/' + filepath, mode='wb') as f:
                        await f.write(await response.read())
                    return True
                except Exception as e:
                    print(f'error in synthesis : {e}')
    except Exception as e:
        print(f'error in session: {e}')
        return False

async def text_to_wav(text):
    global counter
    counter += 1
    if counter > 100:
        counter = 0
    file_name = "temp" + str(counter) + ".wav"
    file_path = './audio_tmp/' + file_name
    result = await genarete_wav(text=text, filepath=file_path)
    if result:
        return file_path
    else:
        "Failed"

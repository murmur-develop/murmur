import discord
from discord.ext import commands
from typing import cast, Any, Coroutine
from voicevox import Voicevox
import asyncio

class SpeakTask:
        message: discord.Message
        source: discord.FFmpegOpusAudio

        def __init__(self, message: discord.Message, source: discord.FFmpegOpusAudio):
            self.message = message
            self.source = source

        @property
        def channel(self):
            return cast(discord.VoiceChannel, self.message.channel)

        @property
        def guild(self):
            return self.message.guild

class Text2SpeechQueue:
    bot: commands.Bot
    voicevox: Voicevox

    queue: list[SpeakTask] = []

    is_running = False
    _tasks: set[asyncio.Task] = set()

    def __init__(self, bot: commands.Bot, voicevox: Voicevox):
        self.bot = bot
        self.voicevox = voicevox

    def add(self, task: SpeakTask):
        self.queue.append(task)
        if not self.is_running:
            self.run()

    def shift(self) -> SpeakTask | None:
        if len(self.queue) <= 0: return None
        return self.queue.pop(0)

    def create_task(self, c: Coroutine):
        task = self.bot.loop.create_task(c)
        self._tasks.add(task)

        task.add_done_callback(self._tasks.discard)

    def run(self):
        def after_fn(prev_result: Exception | None = None):
            if prev_result is not None:
                raise prev_result

            self.create_task(next_fn())

        async def next_fn():
            task = self.shift()
            if task is not None:
                if task.source and type(task.guild.voice_client) is discord.VoiceClient:
                    task.guild.voice_client.play(task.source, after=after_fn)
                else:
                    await task.message.reply('audio failed')
            else:
                self.is_running = False

        if self.is_running: return
        self.is_running = True

        print("-- hogehoge")
        self.create_task(next_fn())
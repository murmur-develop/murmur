from dotenv import load_dotenv
import os
import discord
from commands import ReadingAloud
import asyncio
import logging
from bot import bot

discord.utils.setup_logging(level=logging.INFO, root=False)
load_dotenv()

token = os.environ.get("BOT_TOKEN", "DISCORD_BOT_TOKEN")
host = os.environ.get("VOICEVOX_HOST", "127.0.0.1:50021")

async def main():
    async with bot:
        await bot.add_cog(ReadingAloud(bot))
        await bot.start(token=token)

asyncio.run(main())
from dotenv import load_dotenv
import os
import discord
from commands import ReadingAloud
import asyncio
import logging
from bot import bot

discord.utils.setup_logging(level=logging.INFO, root=False)

token = os.environ.get("BOT_TOKEN", "DISCORD_BOT_TOKEN")


async def main():
    async with bot:
        await bot.add_cog(ReadingAloud(bot))
        await bot.start(token=token)


asyncio.run(main())

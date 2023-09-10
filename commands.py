import discord
from discord.ext import commands

class ReadingAloud(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        """join voice channel"""
        target_channel = channel
        if target_channel is None:
            target_channel = ctx.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(target_channel)

        await target_channel.connect()
        embed = discord.Embed(
            title="Connect",
            color=discord.Color.brand_green(),
            description="connect yomiage bot",
        )
        embed.set_author(name=self.bot.user)
        await ctx.send(embed=embed)

    @commands.command()
    async def bye(self, ctx):
        """leave voice channel"""
        await ctx.voice_client.disconnect()
        embed = discord.Embed(
            title="Disconnect",
            color=discord.Color.brand_green(),
            description="disconnect yomiage bot",
        )
        embed.set_author(name=self.bot.user)
        await ctx.send(embed=embed)
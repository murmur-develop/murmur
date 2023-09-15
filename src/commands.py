import discord
from discord.ext import commands

class ReadingAloud(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        """join voice channel"""
        target_channel = channel
        if target_channel is None:
            if type(ctx.channel) is not discord.VoiceChannel:
                embed = discord.Embed(
                    title="Error",
                    color=discord.Color.brand_red(),
                    description=(
                        """Not participating in voice channel.
Please join the voice channel or specify a valid channel as an argument."""
                    ),
                )
                embed.set_author(name=self.bot.user)
                await ctx.send(embed=embed)
                return

            target_channel = ctx.channel
        if type(ctx.voice_client) is discord.VoiceClient:
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
    async def bye(self, ctx: commands.Context):
        """leave voice channel"""
        if type(ctx.voice_client) is not discord.VoiceClient:
            embed = discord.Embed(
                title="Error",
                color=discord.Color.brand_red(),
                description="Already left the audio channel.",
            )
            embed.set_author(name=self.bot.user)
            await ctx.send(embed=embed)
            return

        await ctx.voice_client.disconnect()
        embed = discord.Embed(
            title="Disconnect",
            color=discord.Color.brand_green(),
            description="disconnect yomiage bot",
        )
        embed.set_author(name=self.bot.user)
        await ctx.send(embed=embed)
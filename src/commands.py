import discord
from discord import app_commands
from discord.ext import commands


class ReadingAloud(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join", description="botをボイスチャンネルに参加させます")
    @app_commands.describe(channel="参加させるボイスチャンネル(何も入力しない場合は現在のボイスチャンネルに参加します)")
    async def join(
        self,
        interaction: discord.Interaction,
        *,
        channel: discord.VoiceChannel | None = None,
    ):
        """join voice channel"""
        target_channel = channel
        if target_channel is None:
            if type(interaction.channel) is not discord.VoiceChannel:
                embed = discord.Embed(
                    title="Error",
                    color=discord.Color.brand_red(),
                    description=(
                        """Not participating in voice channel.
Please join the voice channel or specify a valid channel as an argument."""
                    ),
                )
                embed.set_author(name=self.bot.user)
                await interaction.response.send_message(embed=embed)
                return

            target_channel = interaction.channel
        if (
            interaction.guild
            and type(interaction.guild.voice_client) is discord.VoiceClient
        ):
            return await interaction.guild.voice_client.move_to(target_channel)

        await target_channel.connect()
        embed = discord.Embed(
            title="Connect",
            color=discord.Color.brand_green(),
            description=f"{self.bot.user}が接続しました",
        )
        embed.set_author(name=self.bot.user)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bye", description="botをボイスチャンネルから退出させます")
    async def bye(self, interaction: discord.Interaction):
        """leave voice channel"""
        if (
            interaction.guild
            and type(interaction.guild.voice_client) is not discord.VoiceClient
        ):
            embed = discord.Embed(
                title="Error",
                color=discord.Color.brand_red(),
                description="Already left the audio channel.",
            )
            embed.set_author(name=self.bot.user)
            await interaction.response.send_message(embed=embed)
            return
        if interaction.guild and interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect(force=True)
        embed = discord.Embed(
            title="Disconnect",
            color=discord.Color.greyple(),
            description=f"{self.bot.user}が退出しました",
        )
        embed.set_author(name=self.bot.user)
        await interaction.response.send_message(embed=embed)

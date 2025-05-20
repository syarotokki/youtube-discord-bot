import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config

class CheckYouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check_youtube", description="YouTubeチャンネルIDが設定されているか確認します")
    async def check_youtube(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)
        yt_id = config.get(guild_id, {}).get("youtube_channel_id")

        if yt_id:
            await interaction.response.send_message(f"📺 現在設定されているYouTubeチャンネルIDは `{yt_id}` です。")
        else:
            await interaction.response.send_message("⚠️ YouTubeチャンネルIDが未設定です。")

async def setup(bot: commands.Bot):
    await bot.add_cog(CheckYouTube(bot))

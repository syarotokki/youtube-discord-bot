import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class UpdateYouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="update_youtube", description="YouTubeチャンネルIDを変更します")
    @app_commands.describe(channel_id="新しいYouTubeチャンネルID")
    async def update_youtube(self, interaction: discord.Interaction, channel_id: str):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 設定が存在しません。まず `/subscribe` を使ってください。")
            return

        config[guild_id]["youtube_channel_id"] = channel_id
        save_config(config)
        await interaction.response.send_message(f"📺 YouTubeチャンネルIDを `{channel_id}` に更新しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateYouTube(bot))

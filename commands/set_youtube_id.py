import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class SetYouTubeID(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_youtube_id", description="通知対象のYouTubeチャンネルIDを変更します")
    @app_commands.describe(youtube_channel_id="新しいYouTubeチャンネルのID")
    async def set_youtube_id(self, interaction: discord.Interaction, youtube_channel_id: str):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 通知設定がまだありません。/subscribe を先に使ってください。")
            return

        config[guild_id]["youtube_channel_id"] = youtube_channel_id
        save_config(config)

        await interaction.response.send_message(f"✅ YouTubeチャンネルIDを `{youtube_channel_id}` に変更しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(SetYouTubeID(bot))

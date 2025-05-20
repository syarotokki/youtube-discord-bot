import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_FILE = "config.json"

class ShowConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_config", description="現在の通知設定を表示します")
    async def show_config(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        if not os.path.exists(CONFIG_FILE):
            await interaction.response.send_message("⚠️ 設定ファイルが存在しません。")
            return

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ このサーバーには通知設定がありません。")
            return

        yt_id = config[guild_id]["youtube_channel_id"]
        notify_ch = config[guild_id]["notify_channel_id"]

        await interaction.response.send_message(
            f"🔧 通知設定:\nYouTubeチャンネルID: `{yt_id}`\n通知チャンネル: <#{notify_ch}>"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowConfig(bot))

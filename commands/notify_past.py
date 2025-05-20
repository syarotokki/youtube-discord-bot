import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from utils.youtube import fetch_all_videos
from utils.logger import logger

CONFIG_FILE = "config.json"

class NotifyPast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_past", description="過去の動画をすべて通知します")
    async def notify_past(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild_id = str(interaction.guild.id)

        if not os.path.exists(CONFIG_FILE):
            await interaction.followup.send("❌ 設定ファイルが存在しません。`/subscribe` で先に登録してください。")
            return

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        if guild_id not in config:
            await interaction.followup.send("⚠️ このサーバーには通知設定がありません。")
            return

        yt_channel_id = config[guild_id]["youtube_channel_id"]
        notify_channel = self.bot.get_channel(config[guild_id]["notify_channel_id"])

        try:
            videos = fetch_all_videos(yt_channel_id)
            if not videos:
                await interaction.followup.send("📭 過去動画が見つかりませんでした。")
                return

            for video in videos:
                message = f"📺 **{video['title']}**\nhttps://www.youtube.com/watch?v={video['video_id']}"
                await notify_channel.send(message)

            await interaction.followup.send(f"✅ 合計 {len(videos)} 件の動画を通知しました。")
        except Exception as e:
            logger.error(f"/notify_past エラー: {e}")
            await interaction.followup.send("❌ エラーが発生しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(NotifyPast(bot))

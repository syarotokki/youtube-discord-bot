import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from utils.youtube import fetch_latest_video
from utils.logger import logger

CONFIG_FILE = "config.json"

class NotifyLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_latest", description="最新の動画またはライブを今すぐ通知します")
    async def notify_latest(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild_id = str(interaction.guild.id)

        if not os.path.exists(CONFIG_FILE):
            await interaction.followup.send("❌ 設定ファイルが存在しません。`/subscribe` で先に登録してください。")
            return

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        if guild_id not in config:
            await interaction.followup.send("⚠️ このサーバーには通知設定がありません。`/subscribe` で登録してください。")
            return

        yt_channel_id = config[guild_id]["youtube_channel_id"]
        notify_channel = self.bot.get_channel(config[guild_id]["notify_channel_id"])

        try:
            latest_video = fetch_latest_video(yt_channel_id)
            if latest_video:
                title = latest_video["title"]
                url = f"https://www.youtube.com/watch?v={latest_video['video_id']}"
                is_live = latest_video["is_live"]

                message = f"📢 **{'ライブ配信が始まりました' if is_live else '新しい動画が投稿されました'}**\n**{title}**\n{url}"
                await notify_channel.send(message)
                await interaction.followup.send("✅ 通知を送信しました。")
            else:
                await interaction.followup.send("⚠️ 新しい動画やライブは見つかりませんでした。")
        except Exception as e:
            logger.error(f"/notify_latest でエラー: {e}")
            await interaction.followup.send("❌ エラーが発生しました。ログを確認してください。")

async def setup(bot: commands.Bot):
    await bot.add_cog(NotifyLatest(bot))

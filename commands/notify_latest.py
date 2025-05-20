import discord
from discord.ext import commands
from discord import app_commands
import json
import os

from utils.youtube import fetch_latest_video, fetch_video_details, is_livestream, convert_to_jst
from utils.checks import is_developer

CONFIG_FILE = "config.json"

class NotifyLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_latest", description="登録されたすべてのチャンネルの最新動画を通知（開発者専用）")
    async def notify_latest(self, interaction: discord.Interaction):
        if not is_developer(interaction.user.id):
            await interaction.response.send_message("❌ このコマンドは開発者専用です。", ephemeral=True)
            return

        await interaction.response.send_message("⏳ 最新動画を取得しています...", ephemeral=True)

        notified_count = 0

        if not os.path.exists(CONFIG_FILE):
            await interaction.followup.send("❌ config.json が見つかりませんでした。")
            return

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)

        for channel_id, data in config.items():
            youtube_channel_id = data.get("youtube_channel_id")
            notify_channel_id = data.get("notify_channel_id")

            if not youtube_channel_id or not notify_channel_id:
                continue

            discord_channel = self.bot.get_channel(int(notify_channel_id))
            if not discord_channel:
                continue

            video = fetch_latest_video(youtube_channel_id)
            if not video:
                continue

            video_id = video["id"]["videoId"]
            details = fetch_video_details(video_id)
            title = details["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            if is_livestream(details):
                start_time = convert_to_jst(details["liveStreamingDetails"].get("actualStartTime", ""))
                message = f"🔴 ライブ配信が始まりました！\n**{title}**\n開始時刻: {start_time}\n{url}"
            else:
                message = f"📺 新しい動画が投稿されました！\n**{title}**\n{url}"

            await discord_channel.send(message)
            notified_count += 1

        await interaction.followup.send(f"✅ {notified_count} 件のチャンネルに最新動画を通知しました。")

async def setup(bot):
    await bot.add_cog(NotifyLatest(bot))


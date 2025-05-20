# commands/notify_past.py
import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config
from utils.youtube import fetch_all_videos
import datetime

DEVELOPER_ID = 1105948117624434728

class NotifyPast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_past", description="過去の動画を一括で通知します（最大10件）")
    async def notify_past(self, interaction: discord.Interaction):
        if interaction.user.id != DEVELOPER_ID:
            await interaction.response.send_message("❌ このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("❌ このサーバーはまだ /subscribe されていません。", ephemeral=True)
            return

        settings = config[guild_id]
        youtube_channel_id = settings["youtube_channel_id"]
        notify_channel_id = settings["notify_channel_id"]

        videos = fetch_all_videos(youtube_channel_id, max_results=10)
        if not videos:
            await interaction.response.send_message("❌ 動画の取得に失敗しました。", ephemeral=True)
            return

        channel = self.bot.get_channel(int(notify_channel_id))
        if not channel:
            await interaction.response.send_message("❌ 通知チャンネルが見つかりません。", ephemeral=True)
            return

        await interaction.response.send_message("✅ 通知を送信しました。", ephemeral=True)

        for video in reversed(videos):
            video_id = video["id"].get("videoId")
            if not video_id:
                continue

            title = video["snippet"]["title"]
            published_at = video["snippet"]["publishedAt"]
            published_time = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            published_time = published_time.strftime("%Y/%m/%d %H:%M")
            url = f"https://www.youtube.com/watch?v={video_id}"

            is_live = "liveBroadcastContent" in video["snippet"] and video["snippet"]["liveBroadcastContent"] == "live"

            if is_live:
                await channel.send(f"🔴 **過去のライブ配信**\n**{title}**\n開始時刻：{published_time}\n{url}")
            else:
                await channel.send(f"📺 **過去の動画**\n**{title}**\n公開日時：{published_time}\n{url}")

async def setup(bot):
    await bot.add_cog(NotifyPast(bot))


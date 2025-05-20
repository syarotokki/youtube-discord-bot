# commands/notify_latest.py
import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config
from utils.youtube import fetch_latest_video, is_livestream
import datetime

DEVELOPER_ID = 1105948117624434728

class NotifyLatest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_latest", description="登録されたチャンネルの最新動画を即時通知します")
    async def notify_latest(self, interaction: discord.Interaction):
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

        video = fetch_latest_video(youtube_channel_id)
        if not video:
            await interaction.response.send_message("❌ 最新動画が取得できませんでした。", ephemeral=True)
            return

        video_id = video["id"].get("videoId")
        if not video_id:
            await interaction.response.send_message("❌ 最新動画のIDが取得できませんでした。", ephemeral=True)
            return

        title = video["snippet"]["title"]
        published_at = video["snippet"]["publishedAt"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        is_live = "liveBroadcastContent" in video["snippet"] and video["snippet"]["liveBroadcastContent"] == "live"

        channel = self.bot.get_channel(int(notify_channel_id))
        if channel:
            if is_live:
                published_time = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                published_time = published_time.strftime("%Y/%m/%d %H:%M")
                await channel.send(f"🔴 **ライブ配信が始まりました！**\n**{title}**\n開始時刻：{published_time}\n{url}")
            else:
                await channel.send(f"📢 **新しい動画が投稿されました！**\n**{title}**\n{url}")
            await interaction.response.send_message("✅ 通知を送信しました。", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 通知チャンネルが見つかりません。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NotifyLatest(bot))


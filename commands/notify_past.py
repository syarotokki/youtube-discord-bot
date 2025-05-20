import discord
from discord import app_commands
from discord.ext import commands
import json
from utils.youtube import fetch_all_videos, fetch_video_details, is_livestream, get_start_time

class NotifyPastCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_past", description="過去の動画をすべて通知します（開発者専用）")
    async def notify_past(self, interaction: discord.Interaction):
        # 即時応答しておく（3秒ルール対策）
        await interaction.response.send_message("⏳ 通知処理を開始します...", ephemeral=True)

        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        notified_count = 0

        for channel_id, data in config.items():
            discord_channel_id = data["channel"]
            videos = fetch_all_videos(channel_id, max_results=50)

            if not videos:
                continue

            discord_channel = self.bot.get_channel(int(discord_channel_id))
            if not discord_channel:
                continue

            for video in reversed(videos):
                video_id = video["id"].get("videoId")
                if not video_id:
                    continue

                detail = fetch_video_details(video_id)
                if not detail:
                    continue

                title = detail["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={video_id}"

                if is_livestream(detail):
                    start_time = get_start_time(detail)
                    message = f"🔴 ライブ配信が始まりました: **{title}**\n開始時刻: {start_time}\n{url}"
                else:
                    message = f"📺 新しい動画が投稿されました: **{title}**\n{url}"

                await discord_channel.send(message)

            notified_count += 1

        await interaction.followup.send(f"✅ {notified_count} 件のチャンネルに過去動画を通知しました。")

async def setup(bot):
    await bot.add_cog(NotifyPastCommand(bot))


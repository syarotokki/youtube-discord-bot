import discord
from discord import app_commands
from discord.ext import commands
from utils.youtube import fetch_all_videos, is_livestream
from utils.config import load_config
from utils.checks import is_developer
from datetime import datetime, timedelta

class NotifyPast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def convert_to_jst(self, utc_time_str):
        utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        jst_dt = utc_dt + timedelta(hours=9)
        return jst_dt.strftime("%Y/%m/%d %H:%M:%S")

    @app_commands.command(name="notify_past", description="過去の動画やライブ配信をまとめて通知します（開発者専用）")
    async def notify_past(self, interaction: discord.Interaction):
        if not is_developer(interaction):
            await interaction.response.send_message("❌ このコマンドは開発者専用です。", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        config = load_config()
        success = 0

        for guild_id, info in config.items():
            channel_id = info["channel_id"]
            yt_channel_id = info["youtube_channel_id"]
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                continue

            videos = fetch_all_videos(yt_channel_id, max_results=30)
            for video in reversed(videos):
                video_id = video["id"].get("videoId")
                if not video_id:
                    continue

                title = video["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={video_id}"

                if is_livestream(video):
                    start_time = video.get("liveStreamingDetails", {}).get("actualStartTime", "")
                    if start_time:
                        jst_time = self.convert_to_jst(start_time)
                        message = f"🔴 ライブ配信（過去）\n**{title}**\n{url}\n🕒 開始時刻: {jst_time}"
                    else:
                        message = f"🔴 ライブ配信（過去）\n**{title}**\n{url}"
                else:
                    message = f"📺 過去の動画\n**{title}**\n{url}"

                await channel.send(message)
                await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=1))

            success += 1

        await interaction.followup.send(f"✅ {success} 件のチャンネルに過去動画を通知しました。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NotifyPast(bot))

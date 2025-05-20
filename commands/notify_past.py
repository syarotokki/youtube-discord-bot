import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config
from utils.youtube import fetch_all_videos
from utils.checks import is_developer

class NotifyPastCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="notify_past", description="過去のYouTube動画をすべて通知します（開発者限定）")
    async def notify_past(self, interaction: discord.Interaction):
        if not is_developer(interaction):
            await interaction.response.send_message("❌ このコマンドは開発者専用です。", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        config = load_config()
        guild_id = str(interaction.guild_id)
        if guild_id not in config:
            await interaction.followup.send("❌ このサーバーではチャンネルが設定されていません。")
            return

        channel_id = config[guild_id]["youtube_channel_id"]
        notify_channel_id = int(config[guild_id]["notify_channel_id"])
        notify_channel = interaction.guild.get_channel(notify_channel_id)

        if not notify_channel:
            await interaction.followup.send("❌ 通知チャンネルが見つかりません。")
            return

        videos = fetch_all_videos(channel_id)

        count = 0
        for video in reversed(videos):
            snippet = video["snippet"]
            video_id = video["id"].get("videoId")
            if not video_id:
                continue

            title = snippet["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            published_at = snippet["publishedAt"]
            is_live = "liveBroadcastContent" in snippet and snippet["liveBroadcastContent"] == "live"

            if is_live:
                message = f"🔴 **ライブ配信が始まりました！**\n{title}\n{url}\n開始日時: {published_at}"
            else:
                message = f"📢 **新しい動画が公開されました！**\n{title}\n{url}"

            await notify_channel.send(message)
            count += 1

        await interaction.followup.send(f"✅ {count} 件の過去動画を通知しました。")

async def setup(bot):
    await bot.add_cog(NotifyPastCommand(bot))


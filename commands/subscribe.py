import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_FILE = "config.json"

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subscribe", description="YouTubeチャンネルIDと通知先チャンネルを登録します")
    @app_commands.describe(channel_id="YouTubeのチャンネルID（例: UCXXXXXX）")
    async def subscribe(self, interaction: discord.Interaction, channel_id: str):
        guild_id = str(interaction.guild.id)
        notify_channel_id = interaction.channel.id

        # config.json の読み込み
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {}

        # サーバーごとの設定を保存
        config[guild_id] = {
            "youtube_channel_id": channel_id,
            "notify_channel_id": notify_channel_id
        }

        # ファイルへ保存
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        await interaction.response.send_message(
            f"✅ 通知設定を登録しました。\nYouTubeチャンネルID: `{channel_id}`\n通知先: <#{notify_channel_id}>"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Subscribe(bot))

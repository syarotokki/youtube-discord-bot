import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_FILE = "config.json"

class Unsubscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unsubscribe", description="通知設定を削除します")
    async def unsubscribe(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        # 設定ファイルの読み込み
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {}

        # 設定が存在するか確認
        if guild_id in config:
            del config[guild_id]
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            await interaction.response.send_message("🗑️ 通知設定を削除しました。")
        else:
            await interaction.response.send_message("⚠️ このサーバーには通知設定がありません。")

async def setup(bot: commands.Bot):
    await bot.add_cog(Unsubscribe(bot))

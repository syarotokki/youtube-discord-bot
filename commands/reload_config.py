import discord
from discord import app_commands
from discord.ext import commands
import os

class ReloadConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload_config", description="設定ファイルを再読み込みします")
    async def reload_config(self, interaction: discord.Interaction):
        # 特定の条件が必要ならここでチェック（例：管理者かどうか）

        if not os.path.exists("config.json"):
            await interaction.response.send_message("⚠️ 設定ファイルが見つかりません。")
            return

        await interaction.response.send_message("🔄 設定ファイルを再読み込みしました（実際にはボットのロジックに依存します）。")

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadConfig(bot))

import discord
from discord import app_commands
from discord.ext import commands
import logging

class LogLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="log_level", description="ログレベルを変更します（例: DEBUG, INFO）")
    @app_commands.describe(level="ログレベル名")
    async def log_level(self, interaction: discord.Interaction, level: str):
        try:
            numeric_level = getattr(logging, level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError

            logging.getLogger().setLevel(numeric_level)
            await interaction.response.send_message(f"✅ ログレベルを `{level.upper()}` に変更しました。")
        except Exception:
            await interaction.response.send_message("❌ 無効なログレベルです。使用例: DEBUG, INFO, WARNING, ERROR")

async def setup(bot: commands.Bot):
    await bot.add_cog(LogLevel(bot))

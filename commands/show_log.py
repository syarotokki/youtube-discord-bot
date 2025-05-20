import discord
from discord import app_commands
from discord.ext import commands
import logging

class ShowLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.buffer = []

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        handler.emit = self._log_intercept
        logging.getLogger().addHandler(handler)

    def _log_intercept(self, record):
        msg = record.getMessage()
        if len(self.buffer) >= 10:
            self.buffer.pop(0)
        self.buffer.append(msg)

    @app_commands.command(name="show_log", description="最近のログを表示します（最大10件）")
    async def show_log(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ 開発者のみ使用できます。", ephemeral=True)
            return
        if not self.buffer:
            await interaction.response.send_message("📭 ログはまだ記録されていません。")
        else:
            logs = "\n".join(self.buffer)
            await interaction.response.send_message(f"📝 **直近のログ:**\n```\n{logs}\n```")

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowLog(bot))

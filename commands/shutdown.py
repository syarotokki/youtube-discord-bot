import discord
from discord import app_commands
from discord.ext import commands
import sys

class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shutdown", description="Botをシャットダウンします（開発者専用）")
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ 開発者専用です。", ephemeral=True)
            return

        await interaction.response.send_message("👋 Botを終了します。")
        await self.bot.close()
        sys.exit(0)

async def setup(bot: commands.Bot):
    await bot.add_cog(Shutdown(bot))

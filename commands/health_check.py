import discord
from discord import app_commands
from discord.ext import commands

class HealthCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="health_check", description="Botが正常に動作しているか確認します")
    async def health_check(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Botは正常に稼働中です！")

async def setup(bot: commands.Bot):
    await bot.add_cog(HealthCheck(bot))

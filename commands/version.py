import discord
from discord import app_commands
from discord.ext import commands

VERSION = "1.0.0"

class Version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="version", description="Botのバージョンを表示します")
    async def version(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"📦 現在のBotバージョン: `{VERSION}`")

async def setup(bot: commands.Bot):
    await bot.add_cog(Version(bot))

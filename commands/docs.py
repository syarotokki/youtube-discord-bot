import discord
from discord import app_commands
from discord.ext import commands

DOCS_URL = "https://github.com/syarotokki/youtube-discord-bot"

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="docs", description="Botのドキュメント（GitHubなど）を表示します")
    async def docs(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"📖 ドキュメントはこちら: {DOCS_URL}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Docs(bot))

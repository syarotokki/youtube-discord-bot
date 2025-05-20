import discord
from discord import app_commands
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="about", description="このBotの情報を表示します")
    async def about(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "🤖 **YouTube通知Bot**\n最新動画やライブ配信をDiscordに自動通知します。\n開発者: あなた\nGitHub: https://github.com/syarotokki/youtube-discord-bot\nバージョン: `1.0.0`"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(About(bot))

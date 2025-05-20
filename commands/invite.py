import discord
from discord import app_commands
from discord.ext import commands
import os

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite", description="このBotの招待リンクを表示します")
    async def invite(self, interaction: discord.Interaction):
        client_id = os.getenv("CLIENT_ID") or "YOUR_CLIENT_ID"
        invite_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=274877990912&scope=bot%20applications.commands"

        await interaction.response.send_message(
            f"🔗 Botを他のサーバーに招待するには以下のリンクを使ってください:\n{invite_url}"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Invite(bot))

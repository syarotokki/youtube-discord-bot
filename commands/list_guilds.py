import discord
from discord import app_commands
from discord.ext import commands

class ListGuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="list_guilds", description="Botが参加しているサーバー一覧を表示（開発者用）")
    async def list_guilds(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        guilds = self.bot.guilds
        response = "**📋 参加中のサーバー一覧:**\n"
        for guild in guilds:
            response += f"- {guild.name} (`{guild.id}`)\n"

        await interaction.response.send_message(response)

async def setup(bot: commands.Bot):
    await bot.add_cog(ListGuilds(bot))

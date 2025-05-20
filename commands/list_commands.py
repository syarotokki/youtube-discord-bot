import discord
from discord import app_commands
from discord.ext import commands

class ListCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="list_commands", description="現在のスラッシュコマンド一覧を表示します")
    async def list_commands(self, interaction: discord.Interaction):
        commands = interaction.client.tree.get_commands()
        command_names = [f"/{cmd.name} - {cmd.description}" for cmd in commands]
        text = "\n".join(command_names)

        await interaction.response.send_message(f"📋 **コマンド一覧:**\n{text}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ListCommands(bot))

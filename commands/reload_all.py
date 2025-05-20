import discord
from discord import app_commands
from discord.ext import commands

class ReloadAll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload_all", description="すべての拡張機能を再読み込みします（開発者用）")
    async def reload_all(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ 開発者専用です。", ephemeral=True)
            return

        for ext in self.bot.extensions:
            await self.bot.reload_extension(ext)

        await interaction.response.send_message("♻️ すべての拡張機能を再読み込みしました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadAll(bot))

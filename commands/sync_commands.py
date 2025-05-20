import discord
from discord import app_commands
from discord.ext import commands

class SyncCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sync_commands", description="スラッシュコマンドを同期します（管理者用）")
    async def sync_commands(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ あなたはこの操作を行う権限がありません。", ephemeral=True)
            return

        await self.bot.tree.sync()
        await interaction.response.send_message("🔄 スラッシュコマンドを再同期しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(SyncCommands(bot))

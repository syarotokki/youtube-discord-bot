import discord
from discord import app_commands
from discord.ext import commands

class LeaveGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leave_guild", description="指定IDのサーバーから退出（開発者用）")
    @app_commands.describe(guild_id="サーバーのID")
    async def leave_guild(self, interaction: discord.Interaction, guild_id: str):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ このコマンドは開発者のみ使用できます。", ephemeral=True)
            return

        guild = self.bot.get_guild(int(guild_id))
        if guild:
            await guild.leave()
            await interaction.response.send_message(f"👋 `{guild.name}` から退出しました。")
        else:
            await interaction.response.send_message("⚠️ 指定されたサーバーが見つかりません。")

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaveGuild(bot))

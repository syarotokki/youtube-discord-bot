import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config

class IsMuted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="is_muted", description="このサーバーの通知がミュート状態か確認します")
    async def is_muted(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        muted = config.get(guild_id, {}).get("muted", False)

        if muted:
            await interaction.response.send_message("🔕 このサーバーの通知は **ミュート中** です。")
        else:
            await interaction.response.send_message("🔔 このサーバーの通知は **有効** です。")

async def setup(bot: commands.Bot):
    await bot.add_cog(IsMuted(bot))

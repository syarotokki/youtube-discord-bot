import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class UnmuteNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unmute_notify", description="このサーバーの通知を再開します")
    async def unmute_notify(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config or not config[guild_id].get("muted"):
            await interaction.response.send_message("🔔 通知は既に有効です。")
            return

        config[guild_id]["muted"] = False
        save_config(config)

        await interaction.response.send_message("🔔 通知を再開しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(UnmuteNotify(bot))

import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="通知を再開（ミュート解除）します")
    async def unmute(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id in config and config[guild_id].get("muted"):
            config[guild_id]["muted"] = False
            save_config(config)
            await interaction.response.send_message("🔔 通知を再開しました。")
        else:
            await interaction.response.send_message("🔔 通知はすでに有効です。")

async def setup(bot: commands.Bot):
    await bot.add_cog(Unmute(bot))

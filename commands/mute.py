import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mute", description="このサーバーの通知をミュートします")
    async def mute(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 通知設定が見つかりません。まず `/subscribe` で設定してください。")
            return

        config[guild_id]["muted"] = True
        save_config(config)
        await interaction.response.send_message("🔕 通知をミュートしました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))

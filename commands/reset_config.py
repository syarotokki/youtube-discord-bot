import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class ResetConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reset_config", description="このサーバーの通知設定を完全にリセットします")
    async def reset_config(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 設定は存在しません。")
            return

        del config[guild_id]
        save_config(config)

        await interaction.response.send_message("♻️ 通知設定を初期化しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(ResetConfig(bot))

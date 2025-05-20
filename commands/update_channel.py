import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class UpdateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="update_channel", description="通知チャンネルをこのチャンネルに変更します")
    async def update_channel(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 設定が存在しません。まず `/subscribe` を使ってください。")
            return

        config[guild_id]["channel_id"] = str(interaction.channel.id)
        save_config(config)
        await interaction.response.send_message(f"🔁 通知チャンネルを {interaction.channel.mention} に更新しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateChannel(bot))

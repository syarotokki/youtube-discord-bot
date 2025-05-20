import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config

class CheckChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check_channel", description="通知チャンネルが存在し、アクセス可能かを確認します")
    async def check_channel(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)
        channel_id = config.get(guild_id, {}).get("channel_id")

        if not channel_id:
            await interaction.response.send_message("⚠️ 通知チャンネルが未設定です。")
            return

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            await interaction.response.send_message("❌ 通知チャンネルが存在しないか、アクセスできません。")
        else:
            await interaction.response.send_message(f"✅ 通知チャンネル {channel.mention} は有効です。")

async def setup(bot: commands.Bot):
    await bot.add_cog(CheckChannel(bot))

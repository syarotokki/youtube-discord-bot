import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

class SetChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_channel", description="通知先チャンネルを変更します")
    @app_commands.describe(channel="新しい通知先チャンネル")
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ 通知設定がまだありません。/subscribe を先に使ってください。")
            return

        config[guild_id]["channel_id"] = str(channel.id)
        save_config(config)

        await interaction.response.send_message(f"✅ 通知チャンネルを {channel.mention} に変更しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(SetChannel(bot))

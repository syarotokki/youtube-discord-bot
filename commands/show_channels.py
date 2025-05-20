import discord
from discord import app_commands
from discord.ext import commands

class ShowChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_channels", description="このサーバーのテキストチャンネル一覧を表示します")
    async def show_channels(self, interaction: discord.Interaction):
        channels = [
            f"- {channel.name} (<#{channel.id}>)"
            for channel in interaction.guild.text_channels
        ]
        channel_list = "\n".join(channels)
        await interaction.response.send_message(f"📺 **テキストチャンネル一覧:**\n{channel_list}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowChannels(bot))

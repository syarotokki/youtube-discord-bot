import discord
from discord import app_commands
from discord.ext import commands
import time

start_time = time.time()

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="uptime", description="Botの稼働時間を表示します")
    async def uptime(self, interaction: discord.Interaction):
        now = time.time()
        delta = int(now - start_time)
        hours = delta // 3600
        minutes = (delta % 3600) // 60
        seconds = delta % 60
        await interaction.response.send_message(f"⏱️ 稼働時間: {hours}h {minutes}m {seconds}s")

async def setup(bot: commands.Bot):
    await bot.add_cog(Uptime(bot))

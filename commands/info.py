import discord
from discord import app_commands
from discord.ext import commands
import psutil, platform, time

start_time = time.time()

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bot_info", description="Botの情報（稼働時間・リソース使用量など）")
    async def info(self, interaction: discord.Interaction):  # ← ここを修正
        uptime = time.time() - start_time
        process = psutil.Process()
        mem = process.memory_info().rss / 1024**2

        embed = discord.Embed(title="🤖 Bot Info", color=0x00BFFF)
        embed.add_field(name="稼働時間", value=f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m", inline=False)
        embed.add_field(name="メモリ使用量", value=f"{mem:.2f} MB", inline=False)
        embed.add_field(name="OS", value=platform.system(), inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotInfo(bot))

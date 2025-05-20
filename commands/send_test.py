import discord
from discord import app_commands
from discord.ext import commands

class SendTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_test", description="テストメッセージを送信します（通知確認）")
    async def send_test(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ テスト通知です。Botは正常に動作しています！")

async def setup(bot: commands.Bot):
    await bot.add_cog(SendTest(bot))

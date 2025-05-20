import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config

class TestNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test_notify", description="通知チャンネルにテストメッセージを送信します")
    async def test_notify(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("⚠️ このサーバーには通知設定がありません。まずは /subscribe してください。")
            return

        channel_id = config[guild_id]["channel_id"]
        channel = self.bot.get_channel(int(channel_id))

        if not channel:
            await interaction.response.send_message("❌ 通知チャンネルが見つかりません。")
            return

        await channel.send("🔔 これは通知テストメッセージです！")
        await interaction.response.send_message("✅ テスト通知を送信しました。")

async def setup(bot: commands.Bot):
    await bot.add_cog(TestNotify(bot))

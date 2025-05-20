import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config

class ShowSubscribers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_subscribers", description="通知を設定しているサーバー一覧（開発者用）")
    async def show_subscribers(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ 開発者のみ使用できます。", ephemeral=True)
            return

        config = load_config()
        if not config:
            await interaction.response.send_message("📭 現在、通知設定されているサーバーはありません。")
            return

        lines = []
        for guild_id, data in config.items():
            lines.append(f"- `{guild_id}` → YouTube: `{data.get('youtube_channel_id', '-')}`")

        response = "\n".join(lines)
        await interaction.response.send_message(f"🔔 **通知設定中のサーバー一覧:**\n{response}")

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowSubscribers(bot))

import discord
from discord import app_commands
from discord.ext import commands
import json
from utils.config import load_config

class ExportConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="export_config", description="設定ファイルをエクスポートします（開発者用）")
    async def export_config(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.client.owner_id:
            await interaction.response.send_message("❌ 開発者のみ使用できます。", ephemeral=True)
            return

        config = load_config()
        json_data = json.dumps(config, indent=2, ensure_ascii=False)
        file = discord.File(fp=discord.File(fp=io.StringIO(json_data), filename="config.json").fp, filename="config.json")

        await interaction.response.send_message("🗂️ 設定ファイルを出力しました：", file=file)

async def setup(bot: commands.Bot):
    await bot.add_cog(ExportConfig(bot))

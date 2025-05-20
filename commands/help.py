import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="利用可能なコマンド一覧を表示します")
    async def help(self, interaction: discord.Interaction):
        help_text = """
🛠 **利用可能なコマンド一覧**:

📌 設定系:
`/subscribe` - YouTubeチャンネルと通知先を登録  
`/unsubscribe` - 通知設定を削除  
`/show_config` - 現在の設定を表示

📣 通知系:
`/notify_latest` - 最新動画を通知  
`/notify_past` - 過去の動画をすべて通知  

⚙️ その他:
`/ping` - Botの応答速度を確認  
`/help` - このヘルプを表示
"""
        await interaction.response.send_message(help_text)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))

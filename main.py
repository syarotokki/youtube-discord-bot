# main.py

import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
from utils.config import load_config
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 全コマンドをcommandsフォルダから読み込む
command_folder = "commands"
for filename in os.listdir(command_folder):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"{command_folder}.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    await bot.tree.sync()

# FlaskサーバーでPing用に常時起動
keep_alive()

# Discord Botを起動
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)

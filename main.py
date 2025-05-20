# main.py

import os
import discord
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

# .env の読み込み（開発用）
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot起動時の処理
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    await bot.tree.sync()

# 非同期で拡張（コマンド）をロードするメイン関数
async def main():
    # Flaskサーバーを起動（Render用）
    keep_alive()

    # 全コマンドを読み込む
    command_folder = "commands"
    for filename in os.listdir(command_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"{command_folder}.{filename[:-3]}")

    # Botを起動
    await bot.start(os.getenv("DISCORD_TOKEN"))

# 非同期イベントループで実行
if __name__ == "__main__":
    asyncio.run(main())

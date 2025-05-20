import discord
from utils.config import get_config

async def send_log(guild, message, bot):
    config = get_config()
    guild_id = str(guild.id)
    log_channel_id = config.get("subscriptions", {}).get(guild_id, {}).get("log_channel")

    if log_channel_id:
        log_channel = bot.get_channel(int(log_channel_id))
        if log_channel:
            try:
                await log_channel.send(f"[LOG] {message}")
            except discord.Forbidden:
                print(f"ログチャンネルへの送信に失敗しました（権限エラー）: {log_channel_id}")
            except Exception as e:
                print(f"ログチャンネルへの送信に失敗しました: {e}")

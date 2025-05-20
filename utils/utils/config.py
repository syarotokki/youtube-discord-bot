import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_guild_config(guild_id):
    config = load_config()
    return config.get("subscriptions", {}).get(str(guild_id), {})

def set_guild_config(guild_id, guild_config):
    config = load_config()
    config.setdefault("subscriptions", {})[str(guild_id)] = guild_config
    save_config(config)

def get_history():
    config = load_config()
    return config.get("history", {})

def add_to_history(guild_id, video_id):
    config = load_config()
    history = config.setdefault("history", {})
    history.setdefault(str(guild_id), []).append(video_id)
    save_config(config)

def get_api_keys():
    config = load_config()
    return config.get("api_keys", []), config.get("api_index", 0)

def rotate_api_key():
    config = load_config()
    keys = config.get("api_keys", [])
    if not keys:
        return None
    index = (config.get("api_index", 0) + 1) % len(keys)
    config["api_index"] = index
    save_config(config)
    return keys[index]

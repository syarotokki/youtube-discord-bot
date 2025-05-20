import os
import json

CONFIG_FILE = "config.json"

def get_api_keys_from_env():
    env_keys = os.getenv("YOUTUBE_API_KEYS", "")
    return [key.strip() for key in env_keys.split(",") if key.strip()]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "subscriptions": {},
            "history": {},
            "api_index": 0
        }

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["api_keys"] = get_api_keys_from_env() or config.get("api_keys", [])
    return config

def save_config(config):
    config.pop("api_keys", None)  # 保存時には api_keys を除外
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# utils/youtube.py

import os
import requests
import logging

logger = logging.getLogger("bot")

api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEY", "").split(",") if key.strip()]
if not api_keys:
    raise ValueError("❌ YOUTUBE_API_KEY が設定されていません。")

def get_api_key(index):
    return api_keys[index]

def fetch_youtube_data(url_params: dict, endpoint: str = "search") -> dict:
    for i, api_key in enumerate(api_keys):
        params = dict(url_params)
        params["key"] = api_key

        try:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/{endpoint}", params=params)
            data = response.json()

            if response.status_code == 200:
                return data

            if "error" in data:
                reason = data["error"]["errors"][0].get("reason", "")
                if reason == "quotaExceeded":
                    logger.warning(f"⚠️ APIキー {i+1}/{len(api_keys)} がクォータ超過。次を試します。")
                    continue
                else:
                    logger.error(f"❌ YouTube APIエラー: {data['error']}")
                    raise Exception(f"YouTube API error: {data['error']}")
        except requests.RequestException as e:
            logger.exception("❌ YouTube APIリクエストエラー")
            raise e

    logger.error("❌ すべてのAPIキーがクォータ超過またはエラーを返しました。")
    raise RuntimeError("❌ 全てのAPIキーが quotaExceeded またはエラーです。")

def fetch_latest_video(channel_id: str):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": 1,
    }
    data = fetch_youtube_data(url_params)
    items = data.get("items", [])
    return items[0] if items else None

def fetch_all_videos(channel_id: str, max_results: int = 10):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": max(1, min(max_results, 50)),  # API制限に従う
    }
    data = fetch_youtube_data(url_params)
    return data.get("items", [])

def fetch_video_details(video_id: str):
    url_params = {
        "part": "snippet,liveStreamingDetails",
        "id": video_id,
    }
    data = fetch_youtube_data(url_params, endpoint="videos")
    items = data.get("items", [])
    return items[0] if items else None

def is_livestream(video_detail: dict):
    """fetch_video_details() で取得したデータを渡す前提"""
    return "liveStreamingDetails" in video_detail and "actualStartTime" in video_detail["liveStreamingDetails"]


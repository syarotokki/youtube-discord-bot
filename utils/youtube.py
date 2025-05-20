import os
import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("bot")

# 環境変数からAPIキーを読み込む
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

    raise RuntimeError("❌ 全てのAPIキーが quotaExceeded です。")

def fetch_latest_video(channel_id: str):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": 1,
        "type": "video"
    }
    data = fetch_youtube_data(url_params)
    items = data.get("items", [])
    if not items:
        return None
    return items[0]

def fetch_all_videos(channel_id: str, max_results: int = 50):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": max_results,
        "type": "video"
    }
    data = fetch_youtube_data(url_params)
    return data.get("items", [])

def fetch_video_details(video_id: str):
    url_params = {
        "part": "snippet,liveStreamingDetails",
        "id": video_id
    }
    return fetch_youtube_data(url_params, endpoint="videos").get("items", [{}])[0]

def is_livestream(video):
    live_details = video.get("liveStreamingDetails", {})
    return "actualStartTime" in live_details

def convert_to_jst(utc_time_str: str) -> str:
    try:
        dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        jst = dt + timedelta(hours=9)
        return jst.strftime("%Y/%m/%d %H:%M")
    except Exception:
        return "不明"

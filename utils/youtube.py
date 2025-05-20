import os
import requests
import logging

logger = logging.getLogger("bot")

# 環境変数から API キーを読み込む（複数対応）
api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEY", "").split(",") if key.strip()]
if not api_keys:
    raise ValueError("❌ YOUTUBE_API_KEY が設定されていません。")

def get_api_key(index):
    return api_keys[index]

def fetch_youtube_data(url_params: dict) -> dict:
    for i, api_key in enumerate(api_keys):
        params = dict(url_params)
        params["key"] = api_key

        try:
            # search.list or videos.list に対応
            base_url = (
                "https://www.googleapis.com/youtube/v3/videos"
                if "id" in params and "channelId" not in params
                else "https://www.googleapis.com/youtube/v3/search"
            )
            response = requests.get(base_url, params=params)
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
    }
    data = fetch_youtube_data(url_params)

    return data.get("items", [])

def fetch_video_details(video_id: str) -> dict:
    url_params = {
        "part": "snippet,liveStreamingDetails",
        "id": video_id,
    }
    data = fetch_youtube_data(url_params)
    items = data.get("items", [])
    return items[0] if items else {}

def is_livestream(video: dict) -> bool:
    live_details = video.get("liveStreamingDetails", {})
    return "actualStartTime" in live_details

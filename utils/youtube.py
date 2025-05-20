import os
import requests
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("bot")

# 環境変数から複数のAPIキーを読み込み
api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEY", "").split(",") if key.strip()]
if not api_keys:
    raise ValueError("❌ YOUTUBE_API_KEY が設定されていません。")

def get_api_key(index):
    return api_keys[index]

# JSTへの変換関数（今回追加）
def convert_to_jst(utc_str: str) -> str:
    try:
        utc_time = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        jst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
        return jst_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "不明"

# YouTube APIデータを取得（APIキーを順に試す）
def fetch_youtube_data(url_params: dict) -> dict:
    for i, api_key in enumerate(api_keys):
        params = dict(url_params)
        params["key"] = api_key

        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
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

# 最新動画を取得
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

# 複数動画を取得（上限を外したい場合は nextPageToken での繰り返し実装が必要）
def fetch_all_videos(channel_id: str, max_results: int = 50):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": max_results,
    }
    data = fetch_youtube_data(url_params)
    return data.get("items", [])

# 動画詳細情報を取得
def fetch_video_details(video_id: str):
    for i, api_key in enumerate(api_keys):
        params = {
            "part": "snippet,liveStreamingDetails",
            "id": video_id,
            "key": api_key
        }

        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
            data = response.json()

            if response.status_code == 200:
                items = data.get("items", [])
                return items[0] if items else None

            if "error" in data:
                reason = data["error"]["errors"][0].get("reason", "")
                if reason == "quotaExceeded":
                    logger.warning(f"⚠️ APIキー {i+1}/{len(api_keys)} がクォータ超過（詳細取得）。次を試します。")
                    continue
                else:
                    logger.error(f"❌ YouTube APIエラー（詳細取得）: {data['error']}")
                    raise Exception(f"YouTube API error: {data['error']}")
        except requests.RequestException as e:
            logger.exception("❌ YouTube APIリクエストエラー（詳細取得）")
            raise e

    raise RuntimeError("❌ 全てのAPIキーが quotaExceeded（詳細取得）です。")

# ライブ配信かどうか判定
def is_livestream(video):
    live_details = video.get("liveStreamingDetails", {})
    return "actualStartTime" in live_details


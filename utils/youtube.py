import os
import requests
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("bot")

# 複数APIキー対応
api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEY", "").split(",") if key.strip()]
if not api_keys:
    raise ValueError("❌ YOUTUBE_API_KEY が設定されていません。")

def get_api_key(index):
    return api_keys[index]

# JST変換
def convert_to_jst(utc_time_str):
    try:
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        jst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
        return jst_time.strftime("%Y/%m/%d %H:%M:%S")
    except Exception:
        return "不明"

# YouTube APIコール（複数キーに対応）
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

# 動画詳細を取得（動画IDから）
def fetch_video_details(video_id: str) -> dict:
    for i, api_key in enumerate(api_keys):
        try:
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "snippet,liveStreamingDetails",
                    "id": video_id,
                    "key": api_key
                }
            )
            data = response.json()

            if response.status_code == 200 and data["items"]:
                return data["items"][0]

            if "error" in data:
                reason = data["error"]["errors"][0].get("reason", "")
                if reason == "quotaExceeded":
                    logger.warning(f"⚠️ APIキー {i+1}/{len(api_keys)}（動画詳細）がクォータ超過。次を試します。")
                    continue
                else:
                    logger.error(f"❌ YouTube APIエラー（動画詳細）: {data['error']}")
                    raise Exception(f"YouTube API error: {data['error']}")
        except requests.RequestException as e:
            logger.exception("❌ 動画詳細取得エラー")
            raise e

    raise RuntimeError("❌ 全てのAPIキーが（動画詳細） quotaExceeded です。")

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
    if not items:
        return None

    return items[0]

# 複数動画を取得（最大50件まで）
def fetch_all_videos(channel_id: str, max_results: int = 50):
    url_params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": min(max_results, 50),
    }
    data = fetch_youtube_data(url_params)

    return data.get("items", [])

# ライブ配信かどうか判定
def is_livestream(video):
    video_id = video.get("id", {}).get("videoId")
    if not video_id:
        return False
    details = fetch_video_details(video_id)
    return "liveStreamingDetails" in details

# 開始時刻を取得（JST）
def get_start_time(video) -> str:
    video_id = video.get("id", {}).get("videoId")
    if not video_id:
        return "不明"

    details = fetch_video_details(video_id)
    live_details = details.get("liveStreamingDetails", {})
    start_time = live_details.get("actualStartTime") or live_details.get("scheduledStartTime")
    return convert_to_jst(start_time) if start_time else "不明"

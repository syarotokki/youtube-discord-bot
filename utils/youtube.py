import requests
import logging
from utils.config import get_config

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

def get_api_key():
    config = get_config()
    keys = config.get("api_keys", [])
    index = config.get("api_index", 0)
    if not keys:
        raise ValueError("YouTube API キーが設定されていません。")
    return keys[index % len(keys)]

def fetch_latest_videos(channel_id, max_results=5):
    api_key = get_api_key()
    url = f"{YOUTUBE_API_BASE}/search"
    params = {
        "key": api_key,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": max_results
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])

def fetch_video_details(video_id):
    api_key = get_api_key()
    url = f"{YOUTUBE_API_BASE}/videos"
    params = {
        "key": api_key,
        "id": video_id,
        "part": "snippet,liveStreamingDetails"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[0] if items else None

def is_livestream(video):
    live_details = video.get("liveStreamingDetails", {})
    return "actualStartTime" in live_details

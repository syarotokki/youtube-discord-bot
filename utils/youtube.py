import os
import requests
import logging

logger = logging.getLogger("bot")

# 環境変数から複数APIキーを読み込み
api_keys = [key.strip() for key in os.getenv("YOUTUBE_API_KEY", "").split(",") if key.strip()]

if not api_keys:
    raise ValueError("❌ YouTube APIキーが設定されていません。環境変数 YOUTUBE_API_KEY を確認してください。")

def get_api_key(index):
    """インデックスでAPIキーを取得"""
    return api_keys[index]

def fetch_youtube_data(url_params: dict) -> dict:
    """
    複数APIキーを使ってYouTube APIを呼び出し、
    quotaExceeded エラーが出た場合に別のキーでリトライする。
    """
    for i, api_key in enumerate(api_keys):
        params = dict(url_params)
        params["key"] = api_key

        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
            data = response.json()

            if response.status_code == 200:
                return data

            # クォータ制限を検出して次のキーに切り替える
            if "error" in data:
                error_reason = data["error"]["errors"][0].get("reason", "")
                if error_reason == "quotaExceeded":
                    logger.warning(f"⚠️ APIキー {i+1}/{len(api_keys)} がクォータ超過。次のキーを試します。")
                    continue  # 次のキーへ
                else:
                    # その他のエラー（APIキーが無効、認証エラーなど）
                    logger.error(f"❌ YouTube APIエラー: {data['error']}")
                    raise Exception(f"YouTube API error: {data['error']}")

        except requests.RequestException as e:
            logger.exception("❌ YouTube APIリクエスト中に例外が発生しました")
            raise e

    # すべてのキーが使えなかった
    raise RuntimeError("❌ すべてのYouTube APIキーが使えなくなりました（quotaExceeded）")

def is_livestream(video):
    """
    ライブ配信かどうかを判定（liveStreamingDetails.actualStartTime が存在するかどうか）
    """
    live_details = video.get("liveStreamingDetails", {})
    return "actualStartTime" in live_details

def fetch_all_videos(channel_id, max_results=50):
    """
    指定されたチャンネルの過去動画を最大 max_results 件取得
    """
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": min(50, max_results - len(videos)),
            "order": "date",
            "type": "video"
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        data = fetch_youtube_data(params)

        items = data.get("items", [])
        videos.extend(items)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return videos


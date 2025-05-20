import logging

# ロガーを作成
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# コンソールに出力するハンドラ
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 出力フォーマット
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)

# 重複追加防止（すでに同じハンドラがあればスキップ）
if not logger.hasHandlers():
    logger.addHandler(console_handler)

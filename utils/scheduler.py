import asyncio

# 将来的な拡張用：ジョブのスケジューリング管理
class Scheduler:
    def __init__(self):
        self.jobs = {}

    def add_job(self, guild_id, coro, interval_seconds):
        if guild_id in self.jobs:
            self.remove_job(guild_id)

        loop = asyncio.get_event_loop()
        task = loop.create_task(self._run_periodically(coro, interval_seconds))
        self.jobs[guild_id] = task

    def remove_job(self, guild_id):
        if guild_id in self.jobs:
            self.jobs[guild_id].cancel()
            del self.jobs[guild_id]

    async def _run_periodically(self, coro, interval_seconds):
        while True:
            try:
                await coro()
            except Exception as e:
                print(f"[Scheduler] エラー: {e}")
            await asyncio.sleep(interval_seconds)

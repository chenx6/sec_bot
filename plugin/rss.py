from aiocqhttp import Event

from spider.rss import get_360_boardcast
from .base_bot import BaseBot


class Rss(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(message):
            return False
        return 'RSS' in message

    async def reply(self, event: Event) -> str:
        return await get_360_boardcast(False)

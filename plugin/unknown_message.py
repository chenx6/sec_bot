from aiocqhttp import Event

from .base_bot import BaseBot


class Unknown(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        return self.has_at_bot(message)

    async def reply(self, event: Event) -> str:
        return '我听不大懂你在说什么(＞﹏＜)'

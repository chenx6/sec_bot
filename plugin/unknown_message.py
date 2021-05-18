from aiocqhttp import Event
from aiocqhttp.message import Message

from .base_bot import BaseBot


class Unknown(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        # at 了机器人
        if not self.has_at_bot(event, message):
            return False
        # 但是是回复消息
        return not (True in map(lambda seg: seg['type'] == 'reply',
                                Message(message)))

    async def reply(self, event: Event) -> str:
        return '我听不大懂你在说什么(＞﹏＜)'

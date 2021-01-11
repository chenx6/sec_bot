from aiocqhttp import Event

from .base_bot import BaseBot


class WhoAmI(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(message):
            return False
        return '你是谁' in message

    async def reply(self, event: Event) -> str:
        return '我是伪装成二刺猿纸片人美少女的赛棍机器人，用于催大家去打比赛，而不是整天窝宿舍玩游戏。'

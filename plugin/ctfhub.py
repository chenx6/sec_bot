from re import compile

from aiocqhttp import Event

from spider.ctfhub import ctfhub_get_upcoming_event
from .base_bot import BaseBot


class CTFHub(BaseBot):
    """
    通过 CTFHub 获取比赛相关信息
    """
    comp_regex = compile(r'最近的([\d]+)场比赛')

    def __init__(self):
        super()
        super().__init__()
        self.limit = 5

    def reset_bot(self):
        self.limit = 5

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(event, message):
            return False
        if '最近的比赛' in message:
            return True
        elif self.comp_regex.search(message):
            limit_s = self.comp_regex.findall(message)[0]
            self.limit = int(limit_s)
            if self.limit <= 0:
                self.limit = 1
            elif self.limit > 20:
                self.limit = 20
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        competitions = await ctfhub_get_upcoming_event(self.limit)
        self.reset_bot()
        return competitions if len(competitions) != 0 \
            else 'CTFHUB 炸了Σ( ° △ °|||)︴'

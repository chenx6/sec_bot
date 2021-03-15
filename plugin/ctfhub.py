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
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        if not self.has_at_bot(event, message):
            return False
        if '最近的比赛' in message:
            self.session[event.message_id] = 5
            return True
        elif self.comp_regex.search(message):
            limit = int(self.comp_regex.findall(message)[0])
            if limit <= 0:
                limit = 1
            elif limit > 20:
                limit = 20
            self.session[event.message_id] = limit
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        competitions = await ctfhub_get_upcoming_event(
            self.session[event.message_id])
        self.reset_bot(event)
        return competitions if len(competitions) != 0 \
            else 'CTFHUB 炸了Σ( ° △ °|||)︴'

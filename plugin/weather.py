from re import compile

from aiocqhttp import Event

from spider.wttrin import wttrin
from .base_bot import BaseBot


class Weather(BaseBot):
    resp_regex = compile("(.*)([今|明])天天气(如何|怎样)*")
    to_day = {"今": 0, "明": 1}

    def __init__(self):
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        if not self.has_at_bot(event, message):
            return False
        matched = self.resp_regex.search(message)
        if matched == None:
            return False
        self.session[event.message_id] = matched.groups()
        return True

    async def reply(self, event: Event) -> str:
        location, day, _ = self.session[event.message_id]  # type:ignore
        if len(location) == 0:
            location = "青岛"
        try:
            resp = await wttrin(location, self.to_day[day])
        except Exception:
            resp = "获取不到天气..."
        self.reset_bot(event)
        return resp

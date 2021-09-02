from re import compile

from aiocqhttp import Event, Message

from spider.wttrin import wttrin
from .base_bot import BaseBot


class Weather(BaseBot):
    # " *" 吃掉空格，"(.*)"匹配地区
    resp_regex = compile(" *(.*)([今|明])天天气(如何|怎样)*")
    to_day = {"今": 0, "明": 1}

    def __init__(self):
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        if not self.has_at_bot(event, message):
            return False
        # 通过 Message 解析消息，提取出命令文字
        msgs = Message(message)
        msg_lst = list(filter(lambda x: x["type"] == "text", msgs))
        if not msg_lst:
            return False
        text_msg = msg_lst[0]["data"]["text"]
        matched = self.resp_regex.search(text_msg)
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

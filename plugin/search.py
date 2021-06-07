from re import compile

from aiocqhttp import Event

from .base_bot import BaseBot
from spider.bing import bing


class SearchBot(BaseBot):
    """
    搜索引擎机器人
    """

    # 匹配“帮我搜下”，“帮我搜一下”，“帮我搜搜”
    match_regex = compile(r"帮我搜([一]{0,1}下|搜|索)([\w ]{1,30})")

    def __init__(self):
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        if not self.has_at_bot(event, message):
            return False
        matched = self.match_regex.search(message)
        if matched:
            self.session[event.message_id] = matched.group(2)
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        search_result = await bing(self.session[event.message_id])  # type: ignore
        self.reset_bot(event)
        return search_result if len(search_result) else '好像什么都没搜到╮(￣▽￣")╭'

from re import compile

from aiocqhttp import Event

from .base_bot import BaseBot
from spider.bing import bing


class SearchBot(BaseBot):
    """
    搜索引擎机器人
    """

    match_regex = compile("帮我搜下([\w ]{1,30})")

    def __init__(self):
        super().__init__()
        self.reset_bot()

    def reset_bot(self):
        self.keyword = ""

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(event, message):
            return False
        matched = self.match_regex.search(message)
        if matched:
            self.keyword = matched.group(1)
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        search_result = await bing(self.keyword)
        self.reset_bot()
        return search_result if len(search_result) else '好像什么都没搜到╮(￣▽￣")╭'

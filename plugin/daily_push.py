from aiocqhttp import Event

from .base_bot import BaseBot
from spider.rsshub_weibo import get_xuanwu_push


class DailyPush(BaseBot):
    """
    获取腾讯玄武实验室的每日推送
    """
    def __init__(self):
        super()
        super().__init__()
        self.curr_day = True

    def reset_bot(self):
        self.curr_day = True

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(message):
            return False
        if '每日资讯' in message:
            return True
        elif '近期资讯' in message:
            self.curr_day = False
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        article_text = await get_xuanwu_push(self.curr_day)
        self.reset_bot()
        return article_text if len(article_text) != 0 \
                else '怎么抓取不到Σ( ° △ °|||)︴'

from aiocqhttp import Event

from .base_bot import BaseBot
from spider.rsshub_weibo import get_xuanwu_push


class DailyPush(BaseBot):
    """
    获取腾讯玄武实验室的每日推送
    """
    def __init__(self):
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        if not self.has_at_bot(event, message):
            return False
        if '每日资讯' in message:
            self.session[event.message_id] = True
            return True
        elif '近期资讯' in message:
            self.session[event.message_id] = False
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        article_text = await get_xuanwu_push(self.session[event.message_id])  # type: ignore
        self.reset_bot(event)
        return article_text if len(article_text) != 0 \
                else '怎么抓取不到Σ( ° △ °|||)︴'

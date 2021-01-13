from aiocqhttp import Event

from .base_bot import BaseBot


class HelpMenu(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(event, message):
            return False
        return '你能做什么' in message

    async def reply(self, event: Event) -> str:
        return '''我能告诉大家什么时候不要窝在宿舍（最近的比赛，最近的\\d+场比赛），
还能给你推新鲜的资讯，让你知道自己有多菜（每日资讯，近期资讯），
甚至可以搜索漏洞，提醒你该去挖洞刷经验，而不是在宿舍搓手机，对着屏幕傻笑（CVE编号）'''
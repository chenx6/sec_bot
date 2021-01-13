from aiocqhttp import Event

from .base_bot import BaseBot
from config import admin_uid


class Admin(BaseBot):
    """
    管理员命令
    """
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        return self.is_admin(event, message)

    async def reply(self, event: Event) -> str:
        if '测试' in event.message:
            return '我还活着ヽ(✿ﾟ▽ﾟ)ノ'
        elif '清除' in event.message:
            return '清除缓存成功ヽ(✿ﾟ▽ﾟ)ノ'
        else:
            return '......'

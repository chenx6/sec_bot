from aiocqhttp import Event, Message
from aiocqhttp.message import MessageSegment
from config import admin_uid


class BaseBot:
    """
    基础款机器人
    """
    def has_at_bot(self, event: Event, message: str):
        """
        是否有人 at 机器人
        """
        has_at = False
        msg = Message(message)
        for seg in msg:
            if seg == MessageSegment.at(event.self_id):
                has_at = True
        return has_at

    def __init__(self):
        """
        初始化
        """
        pass

    def reset_bot(self):
        """
        重新设置机器人状态
        """
        pass

    def is_admin(self, event: Event, message: str) -> bool:
        return self.has_at_bot(event, message) \
            and event.sender['user_id'] == admin_uid

    def match(self, event: Event, message: str) -> bool:
        """
        查看当前消息是否能处理
        """
        return False

    async def reply(self, event: Event) -> str:
        """
        回复
        """
        return ''

from aiocqhttp import Event
from config import uid


class BaseBot:
    """
    基础款机器人
    """
    at_msg = f'[CQ:at,qq={uid}]'  # at 消息的酷 Q 码

    def has_at_bot(self, message: str):
        """
        是否有人 at 机器人
        """
        return self.at_msg in message

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

from typing import Callable, List
from dataclasses import dataclass
from logging import getLogger

from schedule import Job

logger = getLogger('tools')


@dataclass
class Subscription:
    """
    推送类，记录推送内容，时间，群组
    """

    get_message_func: Callable[[], str]  # 获取推送内容的函数
    subscribe_groups: List[int]  # 获取订阅此条推送消息的群组
    job: Job

    def send_message(self, bot):
        """
        推送消息
        """
        try:
            message = self.get_message_func()
            if not message or len(message) < 5:
                return
            for gid in self.subscribe_groups:
                bot.sync.send_group_msg(group_id=gid, message=message)
        except Exception as e:
            logger.error('Push message error')
            logger.error(e)

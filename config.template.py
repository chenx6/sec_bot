from typing import List

from tools import call_async_func, Subscription
from spider.rsshub_weibo import get_xuanwu_push
from spider.rss import get_360_boardcast, get_rss_push
from spider.ctfhub import ctfhub_get_upcoming_event

admin_uid: int = 123456789  # 管理员的 UID


def get_xuanwu_push_sync() -> str:
    """
    获取待推送内容
    """
    return call_async_func(get_xuanwu_push)


def get_360_boardcast_sync() -> str:
    return call_async_func(get_360_boardcast)


def get_seclist_fulldisclose() -> str:
    return call_async_func(get_rss_push("https://seclists.org/rss/fulldisclosure.rss"))


def get_phoronix() -> str:
    return call_async_func(get_rss_push("https://www.phoronix.com/rss.php"))


def get_ctf_event() -> str:
    return call_async_func(ctfhub_get_upcoming_event())


def debug_message() -> str:
    return "测试中。。。"


# 通过 `Subscription` 对象实现指定推送的内容和推送时间，推送群组
# 请不要将奇怪的参数放入 `Subscription` 的初始化函数中
subscribes: List[Subscription] = [
    # Subscription(get_xuanwu_push_sync, [12345678], 'day', '18:00'),
    # Subscription(get_phoronix, [98765432], 'day', '18:00'),
    # Subscription(get_360_boardcast_sync, [12345678], "day", "18:00"),
    # Subscription(get_seclist_fulldisclose, [12345678], "day", "18:00"),
    # Subscription(get_ctf_event, [12345678], "friday", "20:00"),
    # Subscription(debug_message, [12345678], "day", "20:42"),
]

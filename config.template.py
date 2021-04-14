from typing import List

from requests import get

from tools import call_async_func, Subscription
from spider.rsshub_weibo import rsshub_weibo_article
from spider.rss import get_rss_push
from spider.ctfhub import ctfhub_get_upcoming_event

admin_uid: int = 123456789  # 管理员的 UID



async def get_xuanwu_push(curr_day=True) -> str:
    """
    返回玄武实验室每日推送
    """
    return await rsshub_weibo_article(5582522936, '每日安全动态推送', curr_day)


def get_xuanwu_push_sync() -> str:
    """
    获取待推送内容
    """
    return call_async_func(get_xuanwu_push())


async def get_360_boardcast(curr_day: bool = True) -> str:
    """
    获取 360 的通告
    """
    def filter_boardcast(text: str) -> bool:
        return '通告' in text

    filter_funcs = [filter_boardcast]
    return await get_rss_push('https://cert.360.cn/feed', filter_funcs, curr_day)


def get_360_boardcast_sync() -> str:
    return call_async_func(get_360_boardcast())


def get_seclist_fulldisclose() -> str:
    def filter_malvuln(text: str) -> bool:                                                                    
        return 'malvuln' not in text                                                                          
    lst = [filter_malvuln]                                                                                    
    return call_async_func(get_rss_push("https://seclists.org/rss/fulldisclosure.rss", lst, desc_len=0))


def get_phoronix() -> str:
    return call_async_func(get_rss_push("https://www.phoronix.com/rss.php", desc_len=0))


def get_ctf_event() -> str:
    return call_async_func(ctfhub_get_upcoming_event())


def good_morning() -> str:
    return get('https://wttr.in/Huangdao?format="%l+%c+%t(%f)"').text


def debug_message() -> str:
    return "测试中。。。"


# 通过 `Subscription` 对象实现指定推送的内容和推送时间，推送群组
# 请不要将奇怪的参数放入 `Subscription` 的初始化函数中
subscribes: List[Subscription] = [
    # Subscription(get_xuanwu_push_sync, [12345678], 'day', '18:00'),
    # Subscription(good_morning, [959613860], 'day', '06:30'),
    # Subscription(get_phoronix, [98765432], 'day', '18:00'),
    # Subscription(get_360_boardcast_sync, [12345678], "day", "18:00"),
    # Subscription(get_seclist_fulldisclose, [12345678], "day", "18:00"),
    # Subscription(get_ctf_event, [12345678], "friday", "20:00"),
    # Subscription(debug_message, [12345678], "day", "20:42"),
]

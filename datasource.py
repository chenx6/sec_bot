from datetime import timedelta

from requests import get
from feedparser import FeedParserDict

from utils.call_async import call_async_func
from spider.rsshub_weibo import rsshub_weibo_article
from spider.rss import get_rss_push
from spider.ctfhub import ctfhub_get_upcoming_event
from spider.wttrin import wttrin


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


async def get_360_boardcast(elapse: timedelta = timedelta(days=1)) -> str:
    """
    获取 360 的通告
    """
    def filter_boardcast(item: FeedParserDict) -> bool:
        return '通告' in item.title

    filter_funcs = [filter_boardcast]
    return await get_rss_push('https://cert.360.cn/feed', filter_funcs,
                              elapse, desc_len=100)


def get_360_boardcast_sync() -> str:
    return call_async_func(get_360_boardcast())


def get_seclist_fulldisclose() -> str:
    def filter_malvuln(item: FeedParserDict) -> bool:
        return 'malvuln' not in item.title

    lst = [filter_malvuln]
    return call_async_func(
        get_rss_push("https://seclists.org/rss/fulldisclosure.rss",
                     lst,
                     desc_len=0))


def get_phoronix() -> str:
    return call_async_func(
        get_rss_push("https://www.phoronix.com/rss.php", item_limit=5, desc_len=0))


def get_ctf_event() -> str:
    return call_async_func(ctfhub_get_upcoming_event())


def good_morning() -> str:
    return get('https://wttr.in/Huangdao?format="%l+%c+%t(%f)"').text


def good_night() -> str:
    return call_async_func(wttrin("青岛", 1))


def debug_message() -> str:
    return "测试中。。。"
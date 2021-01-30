from typing import Callable, List
from time import strptime, localtime

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def get_items(session: ClientSession, rss_addr: str) -> List[str]:
    """
    解析 RSS ，获取 item 节点
    """
    response = await session.get(rss_addr)
    text = await response.text()
    soup = BeautifulSoup(text, features="lxml-xml")
    return soup.find_all('item')


def get_push_item(items: list, curr_day: bool) -> List[str]:
    """
    解析 item 节点，获取可以推送的节点
    """
    curr_time = localtime()
    ret_item = []
    for item in items:
        if curr_day:
            pub_time = strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %z')
            if curr_time.tm_yday != pub_time.tm_yday or \
                curr_time.tm_year != pub_time.tm_year:
                continue
        text = f'''标题：{item.title.text.strip()}
链接：{item.link.text}
描述：{item.description.text.strip()}
'''
        ret_item.append(text)
    return ret_item


async def get_rss_push(rss_addr: str,
                       filter_funcs: List[Callable[[str], bool]] = None,
                       curr_day: bool = True) -> str:
    """
    获取 RSS 推送
    """
    async with ClientSession() as session:
        items = await get_items(session, rss_addr)
        ret_item = get_push_item(items, curr_day)
        if filter_funcs:
            for func in filter_funcs:
                ret_item = filter(func, ret_item)
        return '\n'.join(ret_item).strip()


async def get_360_boardcast(curr_day: bool = True) -> str:
    """
    获取 360 的通告
    """
    def filter_boardcast(text: str) -> bool:
        return '通告' in text

    filter_funcs = [filter_boardcast]
    return await get_rss_push('https://cert.360.cn/feed', filter_funcs, curr_day)

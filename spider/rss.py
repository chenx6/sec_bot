from typing import Any, Callable, List, Sequence, Optional
from email.utils import parsedate_to_datetime
from arrow import get, now

from aiohttp import ClientSession
from bs4 import BeautifulSoup


def is_curr_day(pub_time) -> bool:
    """
    判断时间是否为同一天
    """
    pub_time_a = get(pub_time).to('local')
    current_time = now()
    return pub_time_a > current_time.shift(hours=-24) and pub_time_a > current_time


async def get_items(session: ClientSession, rss_addr: str) -> List[Any]:
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
    ret_item = []
    for item in items:
        if curr_day:
            pub_time = parsedate_to_datetime(item.pubDate.text)
            if not pub_time:
                continue
            if not is_curr_day(pub_time):
                continue
        text = f'''标题：{item.title.text.strip()}
链接：{item.link.text}
描述：{item.description.text.strip()}
'''
        ret_item.append(text)
    return ret_item


async def get_rss_push(rss_addr: str,
                       filter_funcs: Optional[Sequence[Callable[[str], bool]]] = None,
                       curr_day: bool = True,
                       limit = 3) -> str:
    """
    获取 RSS 推送
    """
    async with ClientSession() as session:
        items = await get_items(session, rss_addr)
        ret_item = get_push_item(items, curr_day)
        filtered_item = iter(ret_item)
        if filter_funcs:
            for func in filter_funcs:
                filtered_item = filter(func, filtered_item)
        ret_item = list(filtered_item)
        if len(ret_item) > limit:
            ret_item = ret_item[:limit]
        return '\n'.join(ret_item).strip()


async def get_360_boardcast(curr_day: bool = True) -> str:
    """
    获取 360 的通告
    """
    def filter_boardcast(text: str) -> bool:
        return '通告' in text

    filter_funcs = [filter_boardcast]
    return await get_rss_push('https://cert.360.cn/feed', filter_funcs, curr_day)

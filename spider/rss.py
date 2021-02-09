from typing import Any, Callable, List, Sequence, Optional
from time import mktime, strptime, localtime, struct_time
from email.utils import parsedate

from aiohttp import ClientSession
from bs4 import BeautifulSoup


def is_curr_day(curr_time: struct_time, pub_time: struct_time) -> bool:
    """
    判断时间是否为同一天

    注意，判断的是中国时区的时间。
    """
    offset = curr_time.tm_gmtoff - pub_time.tm_gmtoff  # 计算时区偏移
    pub_time_s = mktime(pub_time)  # 转换时间为当前时区的 Unix 时间戳
    pub_time = localtime(pub_time_s + offset)  # 加上时区偏移
    return (
        curr_time.tm_yday == pub_time.tm_yday and curr_time.tm_year == pub_time.tm_year
    )


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
    curr_time = localtime()
    ret_item = []
    for item in items:
        if curr_day:
            pub_time = parsedate(item.pubDate.text)
            if not pub_time:
                continue
            pub_time = localtime(mktime(pub_time))
            if not is_curr_day(curr_time, pub_time):
                continue
        text = f'''标题：{item.title.text.strip()}
链接：{item.link.text}
描述：{item.description.text.strip()}
'''
        ret_item.append(text)
    return ret_item


async def get_rss_push(rss_addr: str,
                       filter_funcs: Optional[Sequence[Callable[[str], bool]]] = None,
                       curr_day: bool = True) -> str:
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
        return '\n'.join(filtered_item).strip()


async def get_360_boardcast(curr_day: bool = True) -> str:
    """
    获取 360 的通告
    """
    def filter_boardcast(text: str) -> bool:
        return '通告' in text

    filter_funcs = [filter_boardcast]
    return await get_rss_push('https://cert.360.cn/feed', filter_funcs, curr_day)

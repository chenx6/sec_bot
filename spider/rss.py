from typing import Callable, Sequence, Optional
from itertools import repeat, islice
from datetime import timedelta

from arrow import now, get as get_time
from feedparser import parse, FeedParserDict


def check_time(item: FeedParserDict, elapse: timedelta):
    """
    检查时间是否在范围内
    """
    return now() - get_time(item.published_parsed) <= elapse  # type: ignore


def gene_push_text(item, desc_len: int):
    """
    生成推送内容
    """
    text = f"标题：{item.title}\n链接：{item.link}"
    if desc_len != 0:
        text += f"\n描述：{item.summary[:desc_len]}"
    return text


async def get_rss_push(rss_addr: str,
                       filter_funcs: Optional[Sequence[Callable[
                           [FeedParserDict], bool]]] = None,
                       elapse_time: timedelta = timedelta(days=1),
                       item_limit: int = 3,
                       desc_len: int = 20) -> str:
    """
    获取 RSS 推送

    :param rss_addr: RSS 地址
    :param filter_funcs: 过滤函数
    :param elapse_time: 限制消息发布时间
    :param item_limit: 限制推送消息数量
    :param desc_len: 推送的描述长度
    """
    items = parse(rss_addr)
    result_items = iter(items.entries)
    result_items = filter(lambda x: check_time(x, elapse_time), result_items)
    if filter_funcs != None:
        for func in filter_funcs:
            result_items = filter(func, result_items)
    if item_limit != 0:
        result_items = islice(result_items, item_limit)
    result_items = map(gene_push_text, result_items, repeat(desc_len))
    return "\n".join(result_items)

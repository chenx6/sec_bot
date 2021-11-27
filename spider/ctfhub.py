from typing import Optional
from aiohttp import ClientSession
from json import dumps
from time import strftime, localtime, time


CTFHUB_DOMAIN = 'https://api.ctfhub.com'


def to_strtime(x: int) -> str: return strftime('%m月%d日 %H:%M:%S', (localtime(x)))


def comp_to_str(i) -> str:
    return f'{i["title"]}\n开始时间：{to_strtime(i["start_time"])}\n结束时间：{to_strtime(i["end_time"])}\n'


async def ctfhub_get_upcoming_event(limit=5, offset=0) -> str:
    """
    返回 CTFHUB 接口获取的快开始的比赛
    """
    async with ClientSession() as session:
        params = {"offset": offset, "limit": limit}
        data = dumps(params)
        response = await session.post(CTFHUB_DOMAIN + '/User_API/Event/getUpcoming', data=data)
        json = await response.json()
        if not json['status']:
            return ''
        competitions = map(comp_to_str, json['data']['items'])
        return '\n'.join(competitions).strip()


async def ctfhub_get_event_by_time(start: Optional[int] = None,
                                   end: Optional[int] = None):
    """
    通过时间进行查询赛事
    """
    if not start:
        start = int(time())
    if not end:
        end = start + 604800  # 往后一周
    async with ClientSession() as session:
        data = {"start": start, "end": end}
        response = await session.post(
            f"{CTFHUB_DOMAIN}/User_API/Event/getCalendar", json=data)
        json = await response.json()
        if not json['status']:
            return ''
        it = filter(
            lambda x: x['start_time'] >= start and x['start_time'] < end,
            json['data']['items'])
        it = map(comp_to_str, it)
        return '\n'.join(it).strip()

from aiohttp import ClientSession
from json import dumps
from time import strftime, localtime


CTFHUB_DOMAIN = 'https://api.ctfhub.com'


def to_strtime(x: int) -> str: return strftime('%m月%d日 %H:%M:%S', (localtime(x)))


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
        competitions = []
        for i in json['data']['items']:
            start_time = to_strtime(i['start_time'])
            end_time = to_strtime(i['end_time'])
            competitions.append(f'{i["title"]}\n开始时间：{start_time}\n结束时间：{end_time}\n')
        return '\n'.join(competitions).strip()

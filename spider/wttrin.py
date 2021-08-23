from aiohttp import ClientSession

HEADERS = {"Accept-Language": "zh"}
DAYTOZH = {0: "今天", 1: "明天", 2: "后天"}


async def wttrin(location: str, day: int = 0):
    """
    使用 wttr.in 获取天气

    :param location: 位置，例如“青岛”
    :param day: 日期，`0` 为今天，`1` 为明天
    """
    async with ClientSession() as session:
        response = await session.get(f"http://wttr.in/{location}?format=j1",
                                     headers=HEADERS)
        data = await response.json()
        day_weather = data["weather"][day]
        max_temp, min_temp = day_weather['maxtempC'], day_weather['mintempC']
        morning_weather = day_weather['hourly'][3]['lang_zh'][0]['value']
        return f"{location}{DAYTOZH[day]}温度{min_temp}~{max_temp}°C，{morning_weather}"

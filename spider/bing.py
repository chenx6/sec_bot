from aiohttp import ClientSession
from bs4 import BeautifulSoup

from tools import HEADER

BING_URL = "https://cn.bing.com/search?q={}"
PRIV_HEADER = HEADER.copy()
PRIV_HEADER["Accept"] = "text/html"
PRIV_HEADER["Accept-Language"] = "zh-CN,zh;q=0.8"
PRIV_HEADER["Cookie"] = (
    "EDGE_V=1;"
    "MUID=10281638F63B634B02DA19FBF77862CB;"
    "MUIDB=10281638F63B634B02DA19FBF77862CB;"
    "SRCHD=AF=NOFORM;"
    "SRCHUID=V=2&GUID=0BB8225F246C4496A81FBEFB58F0F059&dmnchg=1;"
    "SRCHUSR=DOB=20210118&T=1611400721000;"
    "SRCHHPGUSR=CW=1278&CH=523&DPR=1&UTC=480&DM=0&HV=1611403053&WTS=63746997521&BRW=M&BRH=M&PLTL=468&PLTA=758&PLTN=161&EXLTT=31;"
    "_UR=OMD=13255701809;"
    "ABDEF=V=13&ABDV=11&MRNB=0&MRB=1611039258638;"
    "ENSEARCH=BENVER=0;"
    "SNRHOP=I=&TS=;"
    "_EDGE_S=SID=1EDC15D4C91F6DD505B11A1CC85C6C64&mkt=zh-cn;"
    "_SS=SID=1EDC15D4C91F6DD505B11A1CC85C6C64&bIm=429;"
    "ipv6=hit=1611406652872"
)


async def bing(keyword: str, result_count=3) -> str:
    """
    通过 Bing 进行搜索

    :param keyword: 搜索关键字
    :param result_count: 搜索条数
    :return: 返回搜索结果
    :rtype: str
    """
    async with ClientSession(headers=PRIV_HEADER) as session:
        response = await session.get(BING_URL.format(keyword))
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        results = soup.find_all("li", class_="b_algo")
        ret_results = []
        for node in results:
            if len(ret_results) == result_count:
                break
            headlines = node.select("div > h2 > a")
            intros = node.select("div[class='b_richcard']") or node.select('p')
            if len(headlines) and len(intros):
                headline = headlines[0].text
                link = headlines[0]["href"]
                intro = intros[0].text
                ret_results.append(f"{headline}\n{intro}\n{link}")
        return "\n\n".join(ret_results)

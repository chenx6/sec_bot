from aiohttp import ClientSession
from asyncio import get_event_loop
from bs4 import BeautifulSoup
from re import compile

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
SOGOU_URL = 'https://weixin.sogou.com/'
SEARCH_PATH = 'weixin?type=1&query='
article_url_reg = compile('account_article_0" href="(.+)">(.+)</a>')
article_url_reg2 = compile(r"url \+= '(.+)';")
clean_reg = compile("<[^>]*>")


async def parse_sogou(session: ClientSession, public_name: str) -> str:
    response = await session.get(SOGOU_URL + SEARCH_PATH + public_name, headers=HEADERS)
    text = await response.text()
    match_result = article_url_reg.search(text)
    if match_result is None or len(match_result.groups()) != 2:
        raise Exception('Get article error!')
    return match_result.group(1)


async def parse_jump(session: ClientSession, jump_url: str) -> str:
    jump_response = await session.get(SOGOU_URL + jump_url)
    jump_page = await jump_response.text()
    if '图中的验证码' in jump_page:
        raise Exception('Anti spider!')
    urls = article_url_reg2.findall(jump_page)
    url = ''.join(urls).replace('@', '')
    return url


async def parse_page(session: ClientSession, url: str):
    article_response = await session.get(url)
    article_text = await article_response.text()
    soup = BeautifulSoup(article_text, features='html.parser')
    paras = soup.select('#js_content > p')
    return '\n'.join(i.text for i in paras)


async def parse_weixin(public_name: str):
    async with ClientSession() as session:
        jump_url = await parse_sogou(session, public_name)
        url = await parse_jump(session, jump_url)
        texts = await parse_page(session, url)
        print(texts)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(parse_weixin('腾讯玄武实验室'))

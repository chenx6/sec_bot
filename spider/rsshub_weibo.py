from aiohttp import ClientSession
from bs4 import BeautifulSoup
from re import compile
from datetime import datetime

RSSHUB_URL = 'https://rsshub.ioiox.com'
WEIBO_PATH = '/weibo/user/{}'
article_link_regex = compile('<a .+href="(.+)"')
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Cookie':
    'UOR=www.techug.com,widget.weibo.com,login.sina.com.cn; SINAGLOBAL=7493829699063.875.1605266569847; '
    'ULV=1605934048430:6:6:5:4338473117841.034.1605934048336:1605929933448; '
    'SUB=_2AkMo5ACKdcPxrARVm_kdxWzjbY1H-jybMWl8An7uJhMyAxh77llfqSVutBF-XMZMONKhWljDb_JSKsmZyhkINBOa; '
    'SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WF0Nrr51I2A_-U61AKJCEpM5JpVF020SonfehnE1h24; '
    'wb_view_log=1920*10801; wb_view_log_7431897110=1920*10801; '
    'webim_unReadCount=%7B%22time%22%3A1605932873342%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0'
    '%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; _s_tentry=-; '
    'Apache=4338473117841.034.1605934048336; WBStorage=8daec78e6a891122|undefined'
}


async def parse_weibo_rss(session: ClientSession,
                          uid: int,
                          condition=None,
                          curr_day=True) -> str:
    """
    提取微博内容
    """
    rsshub_response = await session.get(RSSHUB_URL + WEIBO_PATH.format(uid))
    rsshub_xml = await rsshub_response.text()
    soup = BeautifulSoup(rsshub_xml, 'lxml-xml')
    items = soup.find_all('item')
    link = ''
    for item in items:
        # 获取日期最近的推送
        if condition not in item.text:
            continue
        if curr_day and datetime.now().strftime('%m-%d') not in item.text:
            continue
        link = article_link_regex.findall(item.text)[0]
        break
    return link


async def parse_weibo_article(session: ClientSession, url: str) -> str:
    """
    将文章中的文字提取出来
    """
    article_response = await session.get(url)
    article_html = await article_response.text()
    soup = BeautifulSoup(article_html, features="html.parser")
    paras = soup.select('.WB_editor_iframe_new')  # 选择器选取所有段落
    return paras[0].text if len(paras) != 0 else ''


async def rsshub_weibo_article(uid: int, condition=None, curr_day=True) -> str:
    """
    通过 rsshub 和 weibo 来获取文章
    """
    async with ClientSession(headers=HEADERS) as session:
        article_link = await parse_weibo_rss(session, uid, condition, curr_day)
        article_text = await parse_weibo_article(
            session, article_link) if len(article_link) != 0 else ''
        return article_text.strip()


async def get_xuanwu_push(curr_day=True) -> str:
    """
    返回玄武实验室每日推送
    """
    return await rsshub_weibo_article(5582522936, '每日安全动态推送', curr_day)

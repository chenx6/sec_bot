from re import compile
from spider.anquanke_vuln import search_anquanke_vuln

from aiocqhttp import Event

from .base_bot import BaseBot


class AnquankeVuln(BaseBot):
    """
    通过安全客获取 CVE 的相关信息
    """
    vuln_regex = compile(r'([Cc][Vv][Ee]-\d+-\d+)')

    def __init__(self):
        super()
        super().__init__()
        self.cve_number = ''

    def reset_bot(self):
        self.cve_number = ''

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(message):
            return False
        if self.vuln_regex.search(message):
            self.cve_number = self.vuln_regex.findall(message)[0]
            return True
        else:
            return False

    async def reply(self, event: Event) -> str:
        content = await search_anquanke_vuln(self.cve_number)
        self.reset_bot()
        return content if len(content) != 0 else '安全客服务器变成炸薯条了？'

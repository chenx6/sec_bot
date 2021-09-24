from re import compile
from spider.debian_pkg import debian_pkg

from aiocqhttp import Event

from .base_bot import BaseBot


class DebianPkgBot(BaseBot):
    match_re = compile("/dpkg (.+)")

    def match(self, event: Event, message: str) -> bool:
        if not event.message_id:
            return False
        match_result = self.match_re.findall(message)
        if not match_result:
            return False
        self.session[event.message_id] = match_result[0]
        return True

    async def reply(self, event: Event) -> str:
        content = await debian_pkg(self.session[event.message_id])  # type: ignore
        self.reset_bot(event)
        return content

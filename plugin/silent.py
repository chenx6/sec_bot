from typing import Optional

from aiocqhttp.event import Event
from .base_bot import BaseBot


class Silent(BaseBot):
    """
    静音
    """
    def __init__(self):
        super().__init__()
        self.is_silent_ = False

    def is_silent(self, event: Optional[Event] = None, message: Optional[str] = None):
        if not event or not message:
            return self.is_silent_
        silent = False
        if self.is_silent_:
            silent = True
        if self.match(event, message):
            silent = False
        return silent

    def match(self, event: Event, message: str) -> bool:
        can_process = False
        if self.is_admin(event, message) and self.has_at_bot(event, message):
            if '休息' in event.message:
                can_process = True
            elif '干活' in event.message:
                can_process = True
        return can_process

    async def reply(self, event: Event) -> str:
        if '休息' in event.message:
            self.is_silent_ = True
            return '我休息一会儿(￣o￣) . z Z'
        elif '干活' in event.message:
            self.is_silent_ = False
            return '(～o￣▽￣)～o ~。。。 '

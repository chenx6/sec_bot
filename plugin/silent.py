from aiocqhttp.event import Event
from .base_bot import BaseBot


class Silent(BaseBot):
    """
    静音
    """
    def __init__(self):
        super().__init__()
        self.is_silent = False

    def match(self, event: Event, message: str) -> bool:
        if self.is_admin(event, message) and self.has_at_bot(event, message):
            if '休息' in event.message:
                self.is_silent = True
            elif '干活' in event.message:
                self.is_silent = False
        return self.is_silent

    def reply(self, event: Event) -> str:
        if '休息' in event.message:
            return '我休息一会儿(￣o￣) . z Z'
        elif '干活' in event.message:
            return '(～o￣▽￣)～o ~。。。 '

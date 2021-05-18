from random import randint

from aiocqhttp import Event, MessageSegment

from .base_bot import BaseBot
from config import lsp_imgs


class LSP(BaseBot):
    imgs = lsp_imgs

    def __init__(self):
        super().__init__()

    def match(self, event: Event, message: str) -> bool:
        return "/lsp" in message

    async def reply(self, event: Event):
        return MessageSegment.image(f"file://{self.imgs[randint(1, len(self.imgs) - 1)]}") \
            if len(self.imgs) else '没图，别想了（ ￣ー￣）'

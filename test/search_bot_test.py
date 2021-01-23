from unittest import TestCase, main

from aiocqhttp import Event

from plugin.search import SearchBot
from tools import call_async_func


class SearchBotTest(TestCase):
    payload = {
        "time": 123,
        "self_id": 123,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": 123,
        "group_id": 123,
        "user_id": 123,
        "message": "[CQ:at,qq=123]帮我搜下聊天机器人",
        "raw_message": "[CQ:at,qq=123]帮我搜下聊天机器人",
        "sender": {"user_id": 123},
    }

    def test1(self):
        event = Event.from_payload(self.payload)
        bot = SearchBot()
        self.assertTrue(bot.match(event, event.message))
        result = call_async_func(bot.reply(event))
        print(result)
        self.assertTrue(len(result) > 20)


if __name__ == "__main__":
    main()

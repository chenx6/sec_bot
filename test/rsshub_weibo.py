from unittest import TestCase, main
from asyncio import get_event_loop

from spider.rsshub_weibo import rsshub_weibo_article
from datasource import get_xuanwu_push
from utils.call_async import call_async_func


class RsshubWeiboSpiderTest(TestCase):
    def test1(self):
        loop = get_event_loop()
        task = loop.create_task(get_xuanwu_push())
        loop.run_until_complete(task)
        result = task.result()
        print(result)
        self.assertTrue(len(result) != 0)

    def test2(self):
        result = call_async_func(rsshub_weibo_article(5582522936, '每日安全动态推送', False))
        print(result)
        self.assertTrue(len(result) != 0)


if __name__ == "__main__":
    main()

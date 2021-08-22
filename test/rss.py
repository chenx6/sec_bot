from unittest import TestCase, main
from datetime import timedelta

from spider.rss import get_rss_push
from datasource import get_360_boardcast
from utils.call_async import call_async_func


class Rss(TestCase):
    def test1(self):
        result = call_async_func(
            get_rss_push('https://seclists.org/rss/fulldisclosure.rss', None,
                         timedelta(days=3)))
        print(result[:20])
        self.assertTrue(len(result) != 0)

    def test2(self):
        result = call_async_func(get_360_boardcast(timedelta(days=7)))
        print(result[:20])
        self.assertTrue(len(result) != 0)

    def test3(self):
        result = call_async_func(
            get_rss_push(
                'https://rsshub.rssforever.com/weibo/user/2803301701'))
        print(result)
        self.assertTrue(isinstance(result, str))


if __name__ == "__main__":
    main()

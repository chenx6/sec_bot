from unittest import TestCase, main

from spider.rss import get_rss_push, get_360_boardcast
from tools import call_async_func


class Rss(TestCase):
    def test1(self):
        result = call_async_func(get_rss_push('https://cert.360.cn/feed'))
        print(result)
        self.assertTrue(len(result) != 0)
    
    def test2(self):
        result = call_async_func(get_360_boardcast(False))
        print(result)
        self.assertTrue(len(result) != 0)


if __name__ == "__main__":
    main()

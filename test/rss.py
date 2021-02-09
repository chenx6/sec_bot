from unittest import TestCase, main

from spider.rss import get_rss_push, get_360_boardcast
from tools import call_async_func


class Rss(TestCase):
    def test1(self):
        result = call_async_func(get_rss_push('https://seclists.org/rss/fulldisclosure.rss', None, False))
        print(result[:20])
        self.assertTrue(len(result) != 0)
    
    def test2(self):
        result = call_async_func(get_360_boardcast(False))
        print(result[:20])
        self.assertTrue(len(result) != 0)
    
    def test3(self):
        result = call_async_func(get_rss_push('https://rsshub.ioiox.com/weibo/user/2803301701'))
        print(result)
        self.assertTrue(isinstance(result, str))


if __name__ == "__main__":
    main()

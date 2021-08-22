from unittest import TestCase, main
from utils.call_async import call_async_func
from spider.bing import bing


class Bing(TestCase):
    def test1(self):
        result = call_async_func(bing("单元测试"))
        print(result)
        self.assertTrue(len(result) != 0)


if __name__ == "__main__":
    main()
from unittest import TestCase, main

from spider.wttrin import wttrin
from utils.call_async import call_async_func


class WttrinTest(TestCase):
    def test_curr_day(self):
        result = call_async_func(wttrin("青岛"))
        print(result)
        self.assertTrue(len(result) != 0)

    def test_next_day(self):
        result = call_async_func(wttrin("青岛", 1))
        print(result)
        self.assertTrue(len(result) != 0)


if __name__ == "__main__":
    main()
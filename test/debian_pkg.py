from unittest import TestCase, main
from utils.call_async import call_async_func
from spider.debian_pkg import debian_pkg


class DebianPkgTest(TestCase):
    def test_source(self):
        result = call_async_func(debian_pkg("plasma-desktop"))
        print(result)
        self.assertTrue(len(result) != 0, result)

    def test_noarch(self):
        result = call_async_func(debian_pkg("plasma-desktop", True))
        print(result)
        self.assertTrue(len(result) != 0, result)

    def test_fail(self):
        result = call_async_func(debian_pkg("wocao"))
        print(result)
        self.assertTrue(len(result) != 0, result)


if __name__ == "__main__":
    main()
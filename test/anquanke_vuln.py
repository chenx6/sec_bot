from unittest import TestCase, main

from spider.anquanke_vuln import search_anquanke_vuln
from tools import call_async_func


class AnquankeVuln(TestCase):
    def test1(self):
        result = call_async_func(search_anquanke_vuln('CVE-2020-0022'))
        print(result)
        self.assertTrue(len(result) != 0)


if __name__ == "__main__":
    main()

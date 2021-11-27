from unittest import TestCase, main
from asyncio import get_event_loop

from spider.ctfhub import ctfhub_get_upcoming_event, ctfhub_get_event_by_time

class CTFHUBSpiderTest(TestCase):
    def test_upcoming_event(self):
        loop = get_event_loop()
        task = loop.create_task(ctfhub_get_upcoming_event())
        loop.run_until_complete(task)
        print(task.result())
        self.assertTrue(len(task.result()) != 0)
    
    def test_ctfhub_time(self):
        loop = get_event_loop()
        task = loop.create_task(ctfhub_get_event_by_time())
        loop.run_until_complete(task)
        print(task.result())
        self.assertTrue(len(task.result()) != 0)


if __name__ == "__main__":
    main()

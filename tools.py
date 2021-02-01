from threading import Thread, Event
from typing import Callable, List
from dataclasses import dataclass
from time import sleep
from schedule import run_pending
from asyncio import new_event_loop, set_event_loop, get_event_loop


HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
}


@dataclass
class Subscription:
    """
    推送类，记录推送内容，时间，群组
    """

    get_message_func: Callable[[], str]  # 获取推送内容的函数
    subscribe_groups: List[int]  # 获取订阅此条推送消息的群组
    send_frequency: str  # 获取发送的频率
    send_time: str  # 获取发送的时间

    def set_bot(self, bot):
        """
        设置发送的 bot 类

        TODO: 优化掉这个函数
        """
        self.bot = bot

    def send_message(self):
        """
        推送消息
        """
        message = self.get_message_func()
        for gid in self.subscribe_groups:
            self.bot.sync.send_group_msg(group_id=gid, message=message)


class LimitCounter:
    """
    发送消息频率限制器
    """
    def __init__(self, limit=5) -> None:
        super().__init__()
        self.count = 0
        self.limit = limit

    def can_send(self) -> bool:
        return self.count < self.limit

    def add_counter(self) -> None:
        self.count += 1

    def reset_counter(self) -> None:
        self.count = 0


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = Event()

    class ScheduleThread(Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                run_pending()
                sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def call_async_func(func):
    """
    Calling async function in sync method
    """
    set_event_loop(new_event_loop())
    loop = get_event_loop()
    task = loop.create_task(func)
    loop.run_until_complete(task)
    return task.result()

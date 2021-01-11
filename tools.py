from threading import Thread, Event
from time import sleep
from schedule import run_pending
from asyncio import new_event_loop, set_event_loop, get_event_loop


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

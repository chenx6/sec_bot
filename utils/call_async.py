from asyncio import new_event_loop, set_event_loop, get_event_loop


def call_async_func(func):
    """
    Calling async function in sync method
    """
    set_event_loop(new_event_loop())
    loop = get_event_loop()
    task = loop.create_task(func)
    loop.run_until_complete(task)
    return task.result()
from typing import List

from aiocqhttp import CQHttp, Event
from schedule import every

from config import subscribe_groups
from tools import run_continuously, call_async_func, LimitCounter
from plugin import (silent, base_bot, anquanke_vuln, ctfhub, daily_push, help_menu,
                    whoami, rss, admin, unknown_message)
from spider.rsshub_weibo import get_xuanwu_push
from spider.ctfhub import ctfhub_get_upcoming_event
from spider.rss import get_360_boardcast

silent_ = silent.Silent()
plugins: List[base_bot.BaseBot] = [
    silent_,
    anquanke_vuln.AnquankeVuln(),
    ctfhub.CTFHub(),
    daily_push.DailyPush(),
    rss.Rss(),
    help_menu.HelpMenu(),
    whoami.WhoAmI(),
    admin.Admin(),
    unknown_message.Unknown()
]
bot = CQHttp()
logger = bot.logger
counter = LimitCounter()


@bot.on_message('group')
async def reply_at(event: Event):
    """
    反馈 at 消息
    """
    if silent_.is_silent(event, event.message):
        return
    if not counter.can_send():
        await bot.send(event, f'发送的太快了吧，{event.sender["nickname"]}，让我缓缓(＞﹏＜)')
        return
    for plugin in plugins:
        if plugin.match(event, event.message):
            try:
                reply_text = await plugin.reply(event)
                await bot.send(event, reply_text)
                counter.add_counter()
            except Exception as e:
                logger.error('Plugin error')
                logger.error(e)
            break


def send_group_boardcast_message(messages: List[str]):
    """
    广播消息到订阅群组
    """
    for m in messages:
        if len(m) < 3:
            continue
        for gid in subscribe_groups:
            bot.sync.send_group_msg(group_id=gid, message=m)


def send_daily_push():
    """
    发送每日推送
    """
    logger.info('Sending daily push')
    try:
        push_items: List[str] = [
            call_async_func(get_xuanwu_push()),
            call_async_func(get_360_boardcast())
        ]
        send_group_boardcast_message(push_items)
    except Exception as e:
        logger.error('Sending daily push error')
        logger.error(e)


def send_weekly_push():
    """
    发送每周推送
    """
    logger.info('Sending weekly push')
    try:
        push_items = [call_async_func(ctfhub_get_upcoming_event())]
        send_group_boardcast_message(push_items)
    except Exception as e:
        logger.error('Sending weekly push error')
        logger.error(e)


def reset_counter():
    counter.reset_counter()


every().day.at('18:00').do(send_daily_push)
every().friday.at('21:00').do(send_weekly_push)
every().minutes.do(reset_counter)
run_continuously(60)
bot.run(host='127.0.0.1', port=8080)

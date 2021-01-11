from typing import List

from aiocqhttp import CQHttp, Event
from schedule import every

from config import subscribe_groups
from tools import run_continuously, call_async_func, LimitCounter
from plugin import (base_bot, anquanke_vuln, ctfhub, daily_push, help_menu,
                    whoami, rss, admin, unknown_message)
from spider.rsshub_weibo import get_xuanwu_push
from spider.ctfhub import ctfhub_get_upcoming_event
from spider.rss import get_360_boardcast

plugins: List[base_bot.BaseBot] = [
    anquanke_vuln.AnquankeVuln(),
    ctfhub.CTFHub(),
    daily_push.DailyPush(),
    rss.Rss(),
    help_menu.HelpMenu(),
    whoami.WhoAmI(),
    admin.Admin(),
    unknown_message.Unknown()
]
send_silent = False  # 机器人禁言
bot = CQHttp()
logger = bot.logger
counter = LimitCounter()


@bot.on_message('group')
async def reply_at(event: Event):
    """
    反馈 at 消息
    """
    if not counter.can_send():
        await bot.send(event, f'发送的太快了吧，{event.sender["nickname"]}，让我缓缓(＞﹏＜)')
        return
    for plugin in plugins:
        if plugin.match(event, event.message):
            reply_text = await plugin.reply(event)
            await bot.send(event, reply_text)
            counter.add_counter()
            break


def send_daily_push():
    """
    发送每日推送
    """
    logger.warning('Sending daily push')
    push_items: List[str] = [
        call_async_func(get_xuanwu_push()),
        call_async_func(get_360_boardcast())
    ]
    for gid in subscribe_groups:
        for p in push_items:
            bot.sync.send_group_msg(group_id=gid, message=p)


def send_weekly_push():
    """
    发送每周推送
    """
    logger.warning('Sending weekly push')
    competitions = call_async_func(ctfhub_get_upcoming_event())
    for gid in subscribe_groups:
        bot.sync.send_group_msg(group_id=gid, message=competitions)


def reset_counter():
    counter.reset_counter()


every().day.at('18:00').do(send_daily_push)
every().friday.at('21:00').do(send_weekly_push)
every().minutes.do(reset_counter)
run_continuously(1800)
bot.run(host='127.0.0.1', port=8080)

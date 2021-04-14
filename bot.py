from typing import List

from aiocqhttp import CQHttp, Event
from schedule import every

from config import subscribes
from tools import run_continuously, LimitCounter
from plugin import (silent, base_bot, anquanke_vuln, ctfhub, daily_push, help_menu,
                    whoami, rss, search, admin, unknown_message)

silent_ = silent.Silent()
plugins: List[base_bot.BaseBot] = [
    silent_,
    anquanke_vuln.AnquankeVuln(),
    ctfhub.CTFHub(),
    daily_push.DailyPush(),
    rss.Rss(),
    help_menu.HelpMenu(),
    whoami.WhoAmI(),
    search.SearchBot(),
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
        if not event.message:
            break
        if plugin.match(event, event.message):
            try:
                reply_text = await plugin.reply(event)
                await bot.send(event, reply_text)
                counter.add_counter()
            except Exception as e:
                logger.error('Plugin error')
                logger.error(e)
            break


def reset_counter():
    counter.reset_counter()


@bot.before_sending
async def can_send_word(event: Event, message, kwargs):
    if silent_.is_silent():
        event.clear()


for s in subscribes:
    s.set_bot(bot)
    # TODO: 找到个比 `eval` 更好的方式来进行添加定时任务。
    exec(f"every().{s.send_frequency}.at('{s.send_time}').do(s.send_message)")
every().minutes.do(reset_counter)
run_continuously(60)
bot.run(host='127.0.0.1', port=8080)

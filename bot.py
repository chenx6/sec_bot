from typing import List

from aiocqhttp import CQHttp, Event
from quart import request
from schedule import every

from config import webhook_token, subscribes
from utils.limit_counter import LimitCounter
from utils.schedule_thread import run_continuously
from plugin import (silent, base_bot, anquanke_vuln, ctfhub, daily_push, help_menu,
                    whoami, rss, search, admin, unknown_message, lsp, weather, debian_pkg)

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
    weather.Weather(),
    debian_pkg.DebianPkgBot(),
    lsp.LSP(),
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


@bot.server_app.route('/webhook')
async def webhook():
    token = request.args.get('token')
    group_id = request.args.get('group_id')
    message = request.args.get('message')
    if not token or token != webhook_token:
        return {"message": "token error"}, 400
    if not group_id or not message:
        return {"message": "error while missing argument"}, 400
    group_id = int(group_id)
    try:
        response = await bot.send_group_msg(group_id=group_id,
                                            message=message)  # type: ignore
        return response
    except Exception as e:
        return {"message": "Server error, " + str(e)}, 500


def reset_counter():
    counter.reset_counter()


@bot.before_sending
async def can_send_word(event: Event, message, kwargs):
    if silent_.is_silent():
        event.clear()

for sub in subscribes:
    sub.job.do(sub.send_message, bot=bot)
every().minutes.do(reset_counter)
run_continuously(60)

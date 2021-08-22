from typing import List
from pathlib import Path

from schedule import every

from datasource import *
from utils.subscription import Subscription

admin_uid: int = 123456789  # 管理员的 UID
webhook_token: str = 'kirakiradokidoki'
lsp_imgs = [str(p.absolute()) for p in Path("images").iterdir()]


# 通过 `Subscription` 对象实现指定推送的内容和推送时间，推送群组
# 时间设定语法请参考 `schedule`
subscribes: List[Subscription] = [
    # Subscription(get_xuanwu_push_sync, [12345678], every().day.at('18:00')),
    # Subscription(good_morning, [959613860], every().day.at('06:30')),
    # Subscription(get_phoronix, [98765432], every().day.at('18:00')),
    # Subscription(get_360_boardcast_sync, [12345678], every().day.at("18:00")),
    # Subscription(get_seclist_fulldisclose, [12345678], every().day.at("18:00")),
    # Subscription(get_ctf_event, [12345678], every().friday.at("20:00")),
    Subscription(debug_message, [12345678], every().day.at("20:42")),
]

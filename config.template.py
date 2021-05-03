from typing import List

from datasource import *
from tools import Subscription

admin_uid: int = 123456789  # 管理员的 UID
webhook_token: str = 'kirakiradokidoki'


# 通过 `Subscription` 对象实现指定推送的内容和推送时间，推送群组
# 请不要将奇怪的参数放入 `Subscription` 的初始化函数中
subscribes: List[Subscription] = [
    # Subscription(get_xuanwu_push_sync, [12345678], 'day', '18:00'),
    # Subscription(good_morning, [959613860], 'day', '06:30'),
    # Subscription(get_phoronix, [98765432], 'day', '18:00'),
    # Subscription(get_360_boardcast_sync, [12345678], "day", "18:00"),
    # Subscription(get_seclist_fulldisclose, [12345678], "day", "18:00"),
    # Subscription(get_ctf_event, [12345678], "friday", "20:00"),
    # Subscription(debug_message, [12345678], "day", "20:42"),
]

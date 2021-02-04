# sec_bot

A QQ bot that boardcast information about cyber security

一个负责推送安全资讯的 QQ 机器人。

## 功能介绍

- 查询 CVE 编号
- 查询最近的 CTF 比赛
- 使用搜索引擎搜索
- 推送 RSS 资源
- 推送每日安全咨询
- 等待添加

## 需要什么

- Python3.7+
- cqhttp 或相关兼容软件

## 如何运行

```bash
# 系统应用配置
# 如果 Python 版本 < 3.7，请使用 pyenv 等软件安装新版本的 Python
apt install python3-pip python3-venv
# 虚拟环境配置
python3 -m venv venv
source venv/bin/activate
# 依赖配置
python3 -m pip install -r requirements.txt
python3 bot.py
```

## 项目介绍

### 项目结构

```plaintext
.
├── bot.py             # 主程序，机器人获取消息，并交给插件处理的地方
├── config.py          # 配置文件，配置管理员，推送信息等参数
├── config.template.py # 配置文件模板
├── LICENSE            # 协议
├── plugin             # 插件目录，存放处理不同信息的插件
├── README.md          # 你正在读的文件
├── requirements.txt   # 让这个程序跑起来的依赖
├── spider             # 信息的来源
├── test               # 单元测试，系统测试
├── tools.py           # 辅助函数存放的地方
└── venv               # 使用 venv 避免污染系统
```

### 插件 (plugin 文件夹中的文件) 介绍

所有的机器人都继承于 "base_bot.py" 中的 `BaseBot`，`BaseBot` 中有其他方法辅助回复判断。在下面的事例中，使用 `match` 方法判断收到的 `message` 是否能处理，如果不能处理，则返回 `False`，能处理时返回 `True`。使用 `reply` 方法则是根据消息进行相应的回复。

下面是一个机器人的演示，当回复中带有 "你是谁" 的字符串时，机器人就回复 "我是伪装成二刺猿纸片人美少女的赛棍机器人..."。

```python
class WhoAmI(BaseBot):
    def __init__(self):
        super()
        super().__init__()

    def reset_bot(self):
        pass

    def match(self, event: Event, message: str) -> bool:
        if not self.has_at_bot(event, message):
            return False
        return '你是谁' in message

    async def reply(self, event: Event) -> str:
        return '我是伪装成二刺猿纸片人美少女的赛棍机器人，用于催大家去打比赛，而不是整天窝宿舍玩游戏。'

```

### 数据来源 (spider 文件夹中的文件) 介绍

机器人回复的内容可能来源是别的网站，所以将信息来源全放在这个文件夹中。在依赖中加入了 `aiohttp` 和 `selenium`，可以作为获取数据的手段。

### 定时任务

使用了 `schedule` 这个库。可以通过在 "config.py" 中的 `subscribes` 列表中添加新的 `Subscription` 对象，达到添加定时任务的方法。

下面是 `Subscription` 类的原型

```python
class Subscription:
    get_message_func: Callable[[], str]  # 获取推送内容的函数
    subscribe_groups: List[int]  # 获取订阅此条推送消息的群组
    send_frequency: str  # 获取发送的频率
    send_time: str  # 获取发送的时间

```

下面是 `subscribes` 类的样例，参数顺序和上方的成员顺序相同。下面的列表定义了在每天的 20:42 分调用 `debug_message` 获取消息，并发给群 12345678 获取的消息。

```python
subscribes: List[Subscription] = [
    Subscription(debug_message, [12345678], "day", "20:42"),
]
```

## TODO

- [ ] 更详细的文档
- [ ] 各种功能的完善
- [ ] Session 的实现
- [ ] 等着添加

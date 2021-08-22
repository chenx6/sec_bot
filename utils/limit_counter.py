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
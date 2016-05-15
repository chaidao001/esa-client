from client.domain.request.request import Request


class Heartbeat(Request):
    def __init__(self):
        super().__init__()
        self._op = "heartbeat"

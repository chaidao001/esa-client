from src.client.domain.request import request


class Heartbeat(request):
    def __init__(self):
        super().__init__()
        self._op = "heartbeat"

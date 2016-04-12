from domain.response import Response


class Connection(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self._connection_id = response["connectionId"]

    @property
    def connectionId(self):
        return self._connection_id

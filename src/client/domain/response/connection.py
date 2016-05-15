from src.client.domain.response import response


class Connection(response):
    def __init__(self, response):
        super().__init__(response["op"])
        self._connection_id = response["connectionId"]

    @property
    def connection_id(self):
        return self._connection_id

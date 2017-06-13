from .response import Response


class Connection(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self.connection_id = response["connectionId"]

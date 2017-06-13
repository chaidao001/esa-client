from .response import Response


class Status(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self.status_code = response["statusCode"]
        if "errorCode" in response:
            self.error_code = response["errorCode"]
        if "errorMessage" in response:
            self.error_message = response["errorMessage"]
        if "connectionClosed" in response:
            self.connection_closed = response["connectionClosed"]

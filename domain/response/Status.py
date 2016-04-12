from domain.response import Response


class Status(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self._status_code = response["statusCode"]
        if "errorCode" in response:
            self._error_code = response["errorCode"]
        if "errorMessage" in response:
            self._error_message = response["errorMessage"]

    @property
    def status_code(self):
        return self._status_code

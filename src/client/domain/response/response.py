class Response:
    def __init__(self, op):
        self._op = op

    def __repr__(self):
        return str(vars(self))

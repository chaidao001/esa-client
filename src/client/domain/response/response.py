class Response:
    def __init__(self, op):
        self.op = op

    def __repr__(self):
        return str(vars(self))

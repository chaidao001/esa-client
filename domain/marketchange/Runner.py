class Runner:
    def __init__(self, response):
        self._id = response["id"]
        self._sort_priority = response["sortPriority"]
        self._status = response["status"]

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    def __repr__(self):
        return str(vars(self))

from enum import Enum


class Runner:
    def __init__(self, response):
        self.id = response["id"]
        self.sort_priority = response["sortPriority"]
        self.status = Runner.RunnerStatus[response["status"]]

    def __repr__(self):
        return str(vars(self))

    class RunnerStatus(Enum):
        ACTIVE, WINNER, LOSER, REMOVED_VACANT, REMOVED, HIDDEN = range(6)

from src.client.domain.marketchange.marketdefinition import MarketDefinition
from src.client.domain.marketchange.runnerchange import RunnerChange


class MarketChange:
    def __init__(self, response):
        self._id = response["id"]
        if "rc" in response:
            self._rc = {rc["id"]: RunnerChange(rc) for rc in response["rc"]}
        else:
            self._rc = dict()
        if "img" in response:
            self._img = response["img"]
        if "marketDefinition" in response:
            self._market_definition = MarketDefinition(response["marketDefinition"])
        if "tv" in response:
            self._tv = response["tv"]

    def update(self, market_change):
        if hasattr(market_change, "market_def"):
            self._market_definition = market_change.market_def

        for runner_id, runner_change in market_change.rc.items():
            if runner_id in self.rc:
                self.rc[runner_id].update(runner_change)
            else:
                self.rc[runner_id] = runner_change

        if hasattr(market_change, "tv"):
            self._tv = market_change.tv

    @property
    def id(self):
        return self._id

    @property
    def rc(self):
        return self._rc

    @property
    def img(self):
        return self._img

    @property
    def market_def(self):
        return self._market_definition

    @property
    def tv(self):
        return self._tv

    def __repr__(self):
        return str(vars(self))

from client.domain.response import Response
from src.client.domain.marketchange.marketchange import MarketChange


class MarketChangeMessage(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self._clk = response["clk"]
        self._pt = response["pt"]
        if "mc" in response:
            self._mc = [MarketChange(mc) for mc in (response["mc"])]
        if "initialClk" in response:
            self._initial_clk = response["initialClk"]
        if "heartbeatMs" in response:
            self._heartbeat_ms = response["heartbeatMs"]
        if "ct" in response:
            self._ct = response["ct"]
        if "conflateMs" in response:
            self._conflate_ms = response["conflateMs"]

    @property
    def initial_clk(self):
        return self._initial_clk

    @property
    def clk(self):
        return self._clk

    @property
    def mc(self):
        return self._mc

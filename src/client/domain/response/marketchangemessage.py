from enum import Enum

from client.domain.marketchange.marketchange import MarketChange
from client.domain.response import Response


class MarketChangeMessage(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self._pt = response["pt"]
        if "clk" in response:
            self._clk = response["clk"]
        if "segmentType" in response:
            self._segment_type = MarketChangeMessage.SegmentType[response["segmentType"]]
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
    def segment_type(self):
        return self._segment_type

    @property
    def mc(self):
        return self._mc

    class SegmentType(Enum):
        SEG_START, SEG, SEG_END = range(3)

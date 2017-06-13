from enum import Enum

from .response import Response
from ..marketchange.marketchange import MarketChange


class MarketChangeMessage(Response):
    def __init__(self, response):
        super().__init__(response["op"])
        self.pt = response["pt"]
        if "clk" in response:
            self.clk = response["clk"]
        if "segmentType" in response:
            self.segment_type = MarketChangeMessage.SegmentType[response["segmentType"]]
        if "mc" in response:
            self.mc = [MarketChange(mc) for mc in (response["mc"])]
        if "initialClk" in response:
            self.initial_clk = response["initialClk"]
        if "heartbeatMs" in response:
            self.heartbeat_ms = response["heartbeatMs"]
        if "ct" in response:
            self.ct = response["ct"]
        if "conflateMs" in response:
            self.conflate_ms = response["conflateMs"]

    class SegmentType(Enum):
        SEG_START, SEG, SEG_END = range(3)

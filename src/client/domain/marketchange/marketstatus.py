from enum import Enum


class MarketStatus(Enum):
    INACTIVE, OPEN, SUSPENDED, CLOSED = range(4)

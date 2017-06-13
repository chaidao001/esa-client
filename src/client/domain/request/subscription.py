from .request import Request


class Subscription(Request):
    def __init__(self):
        super().__init__()
        self.op = "marketSubscription"
        self.clk = None
        self.heartbeat_ms = None
        self.initial_clk = None
        self.market_filter = None
        self.conflate_ms = None
        self.market_data_filter = None

        self.swagger_types = {
            'op': 'str',
            'clk': 'str',
            'heartbeat_ms': 'int',
            'initial_clk': 'str',
            'market_filter': 'MarketFilter',
            'conflate_ms': 'int',
            'id': 'int',
            'market_data_filter': 'MarketDataFilter'
        }

        self.attribute_map = {
            'op': 'op',
            'clk': 'clk',
            'heartbeat_ms': 'heartbeatMs',
            'initial_clk': 'initialClk',
            'market_filter': 'marketFilter',
            'conflate_ms': 'conflateMs',
            'id': 'id',
            'market_data_filter': 'marketDataFilter'
        }

    def to_dict(self):
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            key = self.attribute_map[attr]
            if value:
                if isinstance(value, list):
                    result[key] = list(map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value
                    ))
                elif hasattr(value, "to_dict"):
                    result[key] = value.to_dict()
                else:
                    result[key] = value

        return result

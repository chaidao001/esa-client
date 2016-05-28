from client.domain.request.request import Request


class Subscription(Request):
    def __init__(self):
        super().__init__()
        self._op = "marketSubscription"
        self._clk = None
        self._heartbeat_ms = None
        self._initial_clk = None
        self._market_filter = None
        self._conflate_ms = None
        self._market_data_filter = None

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

    @property
    def clk(self):
        return self._clk

    @clk.setter
    def clk(self, clk):
        self._clk = clk

    @property
    def heartbeat_ms(self):
        return self._heartbeat_ms

    @heartbeat_ms.setter
    def heartbeat_ms(self, heartbeat_ms):
        self._heartbeat_ms = heartbeat_ms

    @property
    def initial_clk(self):
        return self._initial_clk

    @initial_clk.setter
    def initial_clk(self, initial_clk):
        self._initial_clk = initial_clk

    @property
    def market_filter(self):
        return self._market_filter

    @market_filter.setter
    def market_filter(self, market_filter):
        self._market_filter = market_filter

    @property
    def conflate_ms(self):
        return self._conflate_ms

    @conflate_ms.setter
    def conflate_ms(self, conflate_ms):
        self._conflate_ms = conflate_ms

    @property
    def market_data_filter(self):
        return self._market_data_filter

    @market_data_filter.setter
    def market_data_filter(self, market_data_filter):
        self._market_data_filter = market_data_filter

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

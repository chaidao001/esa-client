class MarketFilter:
    def __init__(self):

        self.country_codes = None
        self.betting_types = None
        self.turn_in_play_enabled = None
        self.market_types = None
        self.venues = None
        self.market_ids = None
        self.event_type_ids = None
        self.event_ids = None
        self.bsp_market = None

        self.swagger_types = {
            'country_codes': 'list[str]',
            'betting_types': 'list[str]',
            'turn_in_play_enabled': 'bool',
            'market_types': 'list[str]',
            'venues': 'list[str]',
            'market_ids': 'list[str]',
            'event_type_ids': 'list[str]',
            'event_ids': 'list[str]',
            'bsp_market': 'bool'
        }

        self.attribute_map = {
            'country_codes': 'countryCodes',
            'betting_types': 'bettingTypes',
            'turn_in_play_enabled': 'turnInPlayEnabled',
            'market_types': 'marketTypes',
            'venues': 'venues',
            'market_ids': 'marketIds',
            'event_type_ids': 'eventTypeIds',
            'event_ids': 'eventIds',
            'bsp_market': 'bspMarket'
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

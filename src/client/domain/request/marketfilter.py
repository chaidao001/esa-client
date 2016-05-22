class MarketFilter:
    def __init__(self):

        self._country_codes = None
        self._betting_types = None
        self._turn_in_play_enabled = None
        self._market_types = None
        self._venues = None
        self._market_ids = None
        self._event_type_ids = None
        self._event_ids = None
        self._bsp_market = None

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

    @property
    def country_codes(self):
        return self._country_codes

    @country_codes.setter
    def country_codes(self, country_codes):
        self._country_codes = country_codes

    @property
    def betting_types(self):
        return self._betting_types

    @betting_types.setter
    def betting_types(self, betting_types):
        self._betting_types = betting_types

    @property
    def turn_in_play_enabled(self):
        return self._turn_in_play_enabled

    @turn_in_play_enabled.setter
    def turn_in_play_enabled(self, turn_in_play_enabled):
        self._turn_in_play_enabled = turn_in_play_enabled

    @property
    def market_types(self):
        return self._market_types

    @market_types.setter
    def market_types(self, market_types):
        self._market_types = market_types

    @property
    def venues(self):
        return self._venues

    @venues.setter
    def venues(self, venues):
        self._venues = venues

    @property
    def market_ids(self):
        return self._market_ids

    @market_ids.setter
    def market_ids(self, market_ids: list()):
        self._market_ids = market_ids

    @property
    def event_type_ids(self):
        return self._event_type_ids

    @event_type_ids.setter
    def event_type_ids(self, event_type_ids):
        self._event_type_ids = event_type_ids

    @property
    def event_ids(self):
        return self._event_ids

    @event_ids.setter
    def event_ids(self, event_ids):
        self._event_ids = event_ids

    @property
    def bsp_market(self):
        return self._bsp_market

    @bsp_market.setter
    def bsp_market(self, bsp_market):
        self._bsp_market = bsp_market

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

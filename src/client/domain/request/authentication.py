from .request import Request


class Authentication(Request):
    def __init__(self, app_key, session: str = None):
        super().__init__()
        self.op = "authentication"
        self.app_key = app_key
        self.session = session

        self.swagger_types = {
            'op': 'str',
            'app_key': 'str',
            'id': 'int',
            'session': 'str'
        }

        self.attribute_map = {
            'op': 'op',
            'app_key': 'appKey',
            'id': 'id',
            'session': 'session'
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

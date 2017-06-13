class Request:
    def __init__(self):
        self.op = None
        self.id = None

        self.swagger_types = {
            'op': 'str',
            'id': 'int'
        }

        self.attribute_map = {
            'op': 'op',
            'id': 'id'
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

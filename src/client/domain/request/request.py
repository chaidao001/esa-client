class Request:
    def __init__(self):
        self._op = None
        self._id = None

        self.swagger_types = {
            'op': 'str',
            'id': 'int'
        }

        self.attribute_map = {
            'op': 'op',
            'id': 'id'
        }

    @property
    def op(self):
        return self._op

    @op.setter
    def op(self, op):
        self._op = op

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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

import json


def serialise(message):
    return json.dumps(message.to_dict())


def format_json(message):
    return json.dumps(message, default=lambda o: vars(o), indent=2)


def format_value(value):
    return "{:,}".format(value)


def calculate_book(prices: list()):
    return sum([1 / price for price in prices])


def round_to_2dp(value):
    return round(value * 100) / 100

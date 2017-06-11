import json
from enum import Enum


def serialise(message):
    return json.dumps(message.to_dict())


def format_json(message):
    return json.dumps(message, default=lambda o: o.name if isinstance(o, Enum) else vars(o), indent=2)


def format_to_html(string: str):
    string = string.replace('"_', '"')
    string = string.replace("\n", "<br>")
    string = "<pre>" + string + "</pre>"
    return string


def format_value(value):
    return "{:,}".format(value)


def calculate_book(prices: list()):
    return sum([1 / price for price in prices])


def round_to_2dp(value):
    return round(value * 100) / 100

import json

import requests


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


def get_new_session(username, password, app_key):
    url = 'https://identitysso.betfair.com/api/login'
    data = {'username': username, 'password': password}
    headers = {"Accept": "application/json", "X-Application": app_key}
    req = requests.post(url, headers=headers, data=data)
    return req.json()['token']

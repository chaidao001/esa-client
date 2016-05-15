import requests


def get_new_session(username, password, app_key):
    url = 'https://identitysso.betfair.com/api/login'
    data = {'username': username, 'password': password}
    headers = {"Accept": "application/json", "X-Application": app_key}
    req = requests.post(url, headers=headers, data=data)
    return req.json()['token']

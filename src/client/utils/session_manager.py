from datetime import datetime

import requests

from src.client.utils.configs import Configs


class SessionManager:
    def __init__(self, configs: Configs):
        self._endpoint = configs.sso_endpoint

        self._username = configs.username
        self._password = configs.password
        self._app_key = configs.app_key

        self._session_duration_hour = configs.sso_session_duration_hour

        self._session = None
        self._requested_time = None

    def _get_new_session(self):
        data = {'username': self._username, 'password': self._password}
        headers = {"Accept": "application/json", "X-Application": self._app_key}
        req = requests.post(self._endpoint, headers=headers, data=data)

        self._requested_time = datetime.now()
        self._session = req.json()['token']

    def get_session(self):
        if self._is_expired():
            self._get_new_session()
        return self._session

    def _is_expired(self):
        if not self._requested_time:
            return True

        current_time = datetime.now()
        time_delta = current_time - self._requested_time
        time_delta_hours = time_delta.seconds // 3600

        return time_delta_hours > self._session_duration_hour

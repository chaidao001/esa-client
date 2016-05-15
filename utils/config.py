import configparser
from collections import OrderedDict


class Config:
    def __init__(self):
        self.config_file = "conf/config.ini"

        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.config = config['DEFAULT']

    @property
    def host(self):
        return self.config.get("host")

    @property
    def port(self):
        return self.config.get("port")

    @property
    def heartbeat_interval_second(self):
        return int(self.config.get("heartbeat_interval_second"))

    @property
    def app_key(self):
        return self.config.get("app_key")

    @property
    def username(self):
        return self.config.get("username")

    @property
    def password(self):
        return self.config.get("password")

    @property
    def log_conf(self):
        return self.config.get("log_conf")

    def __repr__(self, *args, **kwargs):
        fields = OrderedDict([("host", self.host),
                              ("port", self.port),
                              ("heartbeat_interval_second", self.heartbeat_interval_second),
                              ("log_conf", self.log_conf)])

        output = ""

        for key, val in fields.items():
            output += "{:28}: {}\n".format(key, val)

        return output

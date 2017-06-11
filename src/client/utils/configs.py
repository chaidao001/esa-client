import configparser
import logging
import logging.config

CONFIG_DIR = "conf/"

class Configs:
    def __init__(self):
        self._cred_config = CredConfig()
        self._env_config = EnvConfig()
        self._app_config = AppConfig()
        self._log_config = LogConfig()

    @property
    def username(self):
        return self._cred_config.username

    @property
    def password(self):
        return self._cred_config.password

    @property
    def app_key(self):
        return self._cred_config.app_key

    @property
    def sso_endpoint(self):
        return self._env_config.sso_endpoint

    @property
    def esa_endpoint(self):
        return self._env_config.esa_endpoint

    @property
    def esa_heartbeat_interval_second(self):
        return self._app_config.esa_heartbeat_interval_second

    @property
    def sso_session_duration_hour(self):
        return self._app_config.sso_session_duration_hour


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(CONFIG_DIR + config_file)

        self._config = config['DEFAULT']

    def read_int_property(self, property_name):
        return int(self.read_property(property_name))

    def read_property(self, property_name):
        return self._config.get(property_name)


class CredConfig(Config):
    def __init__(self):
        self._config_file = "cred.ini"
        super().__init__(self._config_file)

        self.username = self.read_property("username")
        self.password = self.read_property("password")
        self.app_key = self.read_property("app_key")


class EnvConfig(Config):
    def __init__(self):
        self._config_file = "env.ini"
        super().__init__(self._config_file)

        self.sso_endpoint = self.read_property("sso")
        self.esa_endpoint = EnvConfig.Endpoint(self._config, "esa")

    class Endpoint:
        def __init__(self, config: configparser.SectionProxy, server_name: str):
            self.host = config.get(server_name + "_host")
            self.port = int(config.get(server_name + "_port"))


class AppConfig(Config):
    def __init__(self):
        self._config_file = "config.ini"
        super().__init__(self._config_file)

        self.esa_heartbeat_interval_second = self.read_int_property("esa_heartbeat_interval_second")
        self.sso_session_duration_hour = self.read_int_property("sso_session_duration_hour")


class LogConfig:
    def __init__(self):
        self._config_file = CONFIG_DIR + "logging_config.ini"
        logging.config.fileConfig(self._config_file)

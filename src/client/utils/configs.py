import configparser
import logging
import logging.config


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

    @property
    def server_template(self):
        return self._app_config.server_template


class Config:
    def __init__(self, config_file):
        config_dir = "conf/"
        config = configparser.ConfigParser()
        config.read(config_dir + config_file)

        self._config = config['DEFAULT']


class CredConfig(Config):
    def __init__(self):
        self._config_file = "cred.ini"
        super().__init__(self._config_file)

    @property
    def username(self):
        return self._config.get("username")

    @property
    def password(self):
        return self._config.get("password")

    @property
    def app_key(self):
        return self._config.get("app_key")


class EnvConfig(Config):
    def __init__(self):
        self._config_file = "env.ini"
        super().__init__(self._config_file)

    @property
    def sso_endpoint(self):
        return self._config.get("sso")

    @property
    def esa_endpoint(self):
        return EnvConfig.Endpoint(self._config, "esa")

    class Endpoint:
        def __init__(self, config: configparser.SectionProxy, server_name: str):
            self._host = config.get(server_name + "_host")
            self._port = int(config.get(server_name + "_port"))

        @property
        def host(self):
            return self._host

        @property
        def port(self):
            return self._port


class AppConfig(Config):
    def __init__(self):
        self._config_file = "config.ini"
        super().__init__(self._config_file)

    @property
    def esa_heartbeat_interval_second(self):
        return int(self._config.get("esa_heartbeat_interval_second"))

    @property
    def sso_session_duration_hour(self):
        return int(self._config.get("sso_session_duration_hour"))

    @property
    def server_template(self):
        return self._config.get("server_template")


class LogConfig:
    def __init__(self):
        self._config_file = "conf/logging_config.ini"
        logging.config.fileConfig(self._config_file)

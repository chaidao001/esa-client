import logging
import logging.config

from EsaClient import EsaClient
from utils.Config import Config
from utils.utils import get_new_session


def main():
    # loading configs
    config = Config()

    # configuring logger
    logging.config.fileConfig(config.log_conf)
    logging.info("Configs:\n%s" % config)

    app_key = config.app_key

    logging.info("Requesting session token")
    session_token = get_new_session(config.username, config.password, app_key)

    client = EsaClient(config.host, config.port, app_key, session_token, config.heartbeat_interval_second)
    client.init()


if __name__ == "__main__":
    main()

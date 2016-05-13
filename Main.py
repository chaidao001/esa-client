import logging
import logging.config

from EsaClient import EsaClient
from utils.utils import get_default_config, get_new_session


def main():
    # loading configs
    config = get_default_config()

    # configuring logger
    logging.config.fileConfig(config.get('log_conf'))

    app_key = config.get('app_key')

    logging.info("Requesting session token")
    session_token = get_new_session(config.get('username'), config.get('password'), app_key)

    client = EsaClient(config.get('host'), config.get('port'), app_key, session_token)
    client.init()


if __name__ == "__main__":
    main()

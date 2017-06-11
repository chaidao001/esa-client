from src.client.client import EsaClient
from src.client.domain.request.marketfilter import MarketFilter
from src.client.utils.configs import Configs


def main():
    # loading configs
    configs = Configs()

    market_filter = MarketFilter()
    market_filter.market_ids = ["1.132132523"]

    client = EsaClient(configs, market_filter)

    client.init()


if __name__ == "__main__":
    main()

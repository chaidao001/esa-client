from client.domain.marketchange.marketstatus import MarketStatus
from client.domain.marketchange.runner import Runner


class MarketDefinition:
    def __init__(self, response):
        if "bspMarket" in response:
            self._bsp_market = response["bspMarket"]
        if "timezone" in response:
            self._timezone = response["timezone"]
        if "eventId" in response:
            self._event_id = response["eventId"]
        if "suspendTime" in response:
            self._suspend_time = response["suspendTime"]
        if "marketType" in response:
            self._market_type = response["marketType"]
        if "crossMatching" in response:
            self._cross_matching = response["crossMatching"]
        if "inPlay" in response:
            self._in_play = response["inPlay"]
        if "turnInPlayEnabled" in response:
            self._turn_in_play_enabled = response["turnInPlayEnabled"]
        if "eventTypeId" in response:
            self._event_type_id = response["eventTypeId"]
        if "discountAllowed" in response:
            self._discount_allowed = response["discountAllowed"]
        if "betDelay" in response:
            self._bet_delay = response["betDelay"]
        if "status" in response:
            self._status = MarketStatus[response["status"]]
        if "numberOfWinners" in response:
            self._number_of_winners = response["numberOfWinners"]
        if "persistenceEnabled" in response:
            self._persistence_enabled = response["persistenceEnabled"]
        if "bspReconciled" in response:
            self._bsp_reconciled = response["bspReconciled"]
        if "runners" in response:
            self._runners = [Runner(runner) for runner in response["runners"]]
        if "openDate" in response:
            self._open_date = response["openDate"]
        if "countryCode" in response:
            self._country_code = response["countryCode"]
        if "runnersVoidable" in response:
            self._runners_voidable = response["runnersVoidable"]
        if "numberOfActiveRunners" in response:
            self._number_of_active_runners = response["numberOfActiveRunners"]
        if "marketTime" in response:
            self._market_time = response["marketTime"]
        if "complete" in response:
            self._complete = response["complete"]
        if "marketBaseRate" in response:
            self._market_base_rate = response["marketBaseRate"]
        if "version" in response:
            self._version = response["version"]
        if "bettingType" in response:
            self._betting_type = response["bettingType"]

    @property
    def runners(self):
        return self._runners

    @property
    def status(self):
        return self._status

    def __repr__(self):
        return str(vars(self))

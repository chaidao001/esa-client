from .marketstatus import MarketStatus
from .runner import Runner


class MarketDefinition:
    def __init__(self, response):
        if "bspMarket" in response:
            self.bsp_market = response["bspMarket"]
        if "timezone" in response:
            self.timezone = response["timezone"]
        if "eventId" in response:
            self.event_id = response["eventId"]
        if "suspendTime" in response:
            self.suspend_time = response["suspendTime"]
        if "marketType" in response:
            self.market_type = response["marketType"]
        if "crossMatching" in response:
            self.cross_matching = response["crossMatching"]
        if "inPlay" in response:
            self.in_play = response["inPlay"]
        if "turnInPlayEnabled" in response:
            self.turn_in_play_enabled = response["turnInPlayEnabled"]
        if "eventTypeId" in response:
            self.event_type_id = response["eventTypeId"]
        if "discountAllowed" in response:
            self.discount_allowed = response["discountAllowed"]
        if "betDelay" in response:
            self.bet_delay = response["betDelay"]
        if "status" in response:
            self.status = MarketStatus[response["status"]]
        if "numberOfWinners" in response:
            self.number_of_winners = response["numberOfWinners"]
        if "persistenceEnabled" in response:
            self.persistence_enabled = response["persistenceEnabled"]
        if "bspReconciled" in response:
            self.bsp_reconciled = response["bspReconciled"]
        if "runners" in response:
            self.runners = [Runner(runner) for runner in response["runners"]]
        if "openDate" in response:
            self.open_date = response["openDate"]
        if "countryCode" in response:
            self.country_code = response["countryCode"]
        if "runnersVoidable" in response:
            self.runners_voidable = response["runnersVoidable"]
        if "numberOfActiveRunners" in response:
            self.number_of_active_runners = response["numberOfActiveRunners"]
        if "marketTime" in response:
            self.market_time = response["marketTime"]
        if "complete" in response:
            self.complete = response["complete"]
        if "marketBaseRate" in response:
            self.market_base_rate = response["marketBaseRate"]
        if "version" in response:
            self.version = response["version"]
        if "bettingType" in response:
            self.betting_type = response["bettingType"]

    def __repr__(self):
        return str(vars(self))

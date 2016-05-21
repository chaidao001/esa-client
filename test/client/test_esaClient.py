from datetime import datetime
from time import sleep
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from testfixtures import log_capture

from client.client import EsaClient
from client.domain.request.marketfilter import MarketFilter


class TestEsaClient(TestCase):
    def setUp(self):
        self.client = EsaClient(MagicMock(), MagicMock(), MarketFilter())
        conn = Mock()
        self.client._conn = conn

    @log_capture()
    def test_check_no_message_duration_exceedLimit_logWarning(self, captured_logger):
        self.client._timeout_interval_second = 0
        self.client._last_receive_time = datetime.now()
        sleep(1)

        self.client._check_no_message_duration()

        self.assert_have_logging_with_level(captured_logger, "WARNING", "Haven't received any message in 0:00:01")

    @log_capture()
    def test_check_no_message_duration_withinLimit_doNothing(self, captured_logger):
        self.client._timeout_interval_second = 0
        self.client._last_receive_time = datetime.now()

        self.client._check_no_message_duration()

        self.assert_no_logging(captured_logger)

    @log_capture()
    def test_subscribe_withClk_sub(self, captured_logger):
        self.client._clk = 5

        self.client.subscribe()

        self.assert_no_logging_with_level(captured_logger, "INFO")

    @log_capture()
    def test_subscribe_withInitialClk_sub(self, captured_logger):
        self.client._initial_clk = 5

        self.client.subscribe()

        self.assert_no_logging_with_level(captured_logger, "INFO")

    @log_capture()
    def test_subscribe_withoutAnyClk_sub(self, captured_logger):
        self.client.subscribe()

        self.assert_no_logging_with_level(captured_logger, "INFO")

    @log_capture()
    def test_subscribe_withClks_resub(self, captured_logger):
        self.client._initial_clk = 5
        self.client._clk = 10

        self.client.subscribe()

        self.assert_have_logging_with_level(captured_logger, "INFO", "Resubscribing with initial clk 5 and clk 10")

    def assert_no_logging(self, captured_logger):
        records = captured_logger.records
        self.assertEqual(len(records), 0)

    def assert_no_logging_with_level(self, captured_logger, level):
        records = captured_logger.records

        for record in records:
            if record.levelname == level:
                self.fail("{} logger contains message: {}".format(level, record))

    def assert_have_logging_with_level(self, captured_logger, level, expected):
        records = captured_logger.records

        for record in records:
            if record.levelname == level:
                self.assertTrue(expected in records[0].msg)
                return

        self.fail("%s logger does not contain any messages" % level)

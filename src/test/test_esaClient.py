import logging
from datetime import datetime
from time import sleep
from unittest import TestCase

from testfixtures import log_capture

from client.client import EsaClient
from client.domain.request.marketfilter import MarketFilter


class TestEsaClient(TestCase):
    client = None

    def setUp(self):
        self.client = EsaClient("", 8080, "", "", MarketFilter(), 50)

    @log_capture()
    def test_check_no_message_duration_exceedLimit_logWarning(self, captured_logger):
        self.client._timeout_interval_second = 0
        self.client._last_receive_time = datetime.now()

        sleep(1)

        self.client._check_no_message_duration()

        records = captured_logger.records
        self.assertEqual(len(records), 1)
        self.assertTrue("Haven't received any message in 0:00:01" in records[0].msg)

    @log_capture()
    def test_check_no_message_duration_withinLimit_doNothing(self, captured_logger):
        self.client._timeout_interval_second = 0
        self.client._last_receive_time = datetime.now()

        self.client._check_no_message_duration()

        self.assertEqual(0, len(logging.getLogger().handlers[0].records))

        records = captured_logger.records
        self.assertEqual(len(records), 0)

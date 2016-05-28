import json
import logging
import socket
import ssl
import threading
from datetime import datetime
from time import sleep

from client.cache.cache import Cache
from client.domain.request.authentication import Authentication
from client.domain.request.heartbeat import Heartbeat
from client.domain.request.marketfilter import MarketFilter
from client.domain.request.request import Request
from client.domain.request.subscription import Subscription
from client.domain.response.connection import Connection
from client.domain.response.marketchangemessage import MarketChangeMessage
from client.domain.response.status import Status
from client.utils.utils import serialise, format_json
from utils.configs import Configs
from utils.sessionmanager import SessionManager


class EsaClient:
    def __init__(self, configs: Configs, session_manager: SessionManager, market_filter: MarketFilter):
        esa_end_point = configs.esa_endpoint
        self._host = esa_end_point.host
        self._port = esa_end_point.port

        self._app_key = configs.app_key

        self._heartbeat_interval_second = configs.esa_heartbeat_interval_second

        self._session_manager = session_manager
        self._market_filter = market_filter

        self._cache = Cache()
        self._conn = None
        self._connection_id = None
        self._initial_clk = None
        self._clk = None
        self._working = True

        self._last_receive_time = None
        self._timeout_interval_second = 30

    def init(self):
        logging.info('Initialising ESA client')
        self._connect_and_auth()
        self.subscribe()
        self._start_send()

    def _connect_and_auth(self):
        self.connect()
        self.authenticate()

    def _reconnect_and_auth(self):
        logging.info("Re-establishing connection...")
        self.init()

    def _stop_recv_threads(self):
        logging.info("Trying to stop %s" % self._recv_thread.name)
        self._close_socket()

    def _start_recv(self):
        logging.info('Starting to receive messages')
        self._recv_thread = threading.Thread(name="RecvThread", target=self._receive_requests)
        self._recv_thread.start()

    def _start_send(self):
        logging.info('Starting to send heartbeats')

        while self._working:
            try:
                while self._conn and self._working:
                    self.heartbeat()
                    self._check_no_message_duration()
                    sleep(self._heartbeat_interval_second)

                logging.info("Stopped sending")

                if self._working:
                    self._reconnect_and_auth()
            except KeyboardInterrupt:
                logging.warning("KeyboardInterrupt.  Exiting...")

                self._stop_recv_threads()
                while self._recv_thread.is_alive():
                    sleep(1)

    def _check_no_message_duration(self):
        no_message_duration = datetime.now() - self._last_receive_time
        if no_message_duration.seconds > self._timeout_interval_second:
            logging.warning("Haven't received any message in %s" % no_message_duration)

    def _close_socket(self):
        logging.info("Closing socket...")
        try:
            self._conn.shutdown(socket.SHUT_RDWR)
            self._conn.close()
        except Exception as e:
            logging.warning(e)
        finally:
            self._conn = None
            self._connection_id = None

    def _send(self, message: str):
        try:
            self._conn.sendall((message + '\n').encode())
        except socket.error as e:
            logging.error("Error when sending message {}: {}".format(message, e))
            self._stop_recv_threads()

    def _recv(self) -> dict:
        size = 1
        received_message = ''
        packet = None

        while packet != '\n' and self._conn:
            try:
                packet = (self._conn.recv(size)).decode()
            except socket.error as e:
                logging.warning("Error during receiving: %s" % e)
                received_message = ''
                break

            received_message += packet

        if received_message is not '':
            try:
                return json.loads(received_message)
            except Exception as e:
                logging.warning("Failed to deserialise message '{}' because: {}".format(received_message, e))
        else:
            logging.warning("Connection closed")
            self._stop_recv_threads()

    def _receive_requests(self):
        while self._conn:
            self._receive_request()

        logging.info("Stopped receiving")

    def _receive_request(self):
        message = self._recv()
        if message:
            self._process_response(message)

    def _send_request(self, request: Request):
        if request:
            message = serialise(request)
            logging.debug("Sending: %s", message)
            self._send(message)

    def _process_response(self, message: dict):
        op = message["op"]
        self._last_receive_time = datetime.now()

        if op == "connection":
            response = Connection(message)
            self._connection_id = response.connection_id
            logging.info("Connection has been established with ID %s", self._connection_id)
        elif op == "status":
            response = Status(message)
            logging.debug("Received: %s", response)

            if response.connection_closed:
                logging.warning("Connection closed by server: %s" % response)
                self._stop_recv_threads()

            if response.status_code == 'FAILURE':
                logging.warning("Status failure: %s" % response)

        elif op == "mcm":
            response = MarketChangeMessage(message)

            self._update_clk(response)

            if hasattr(response, "segment_type"):
                logging.info("Received segment type: %s" % response.segment_type)

            if hasattr(response, "mc"):
                self._cache.on_receive(response.mc)
                # logging.debug(self._cache.formatted_string())

        else:
            logging.error("Unknown message received: %s" % message)

    def _update_clk(self, response: MarketChangeMessage):
        if hasattr(response, "initial_clk"):
            self._initial_clk = response.initial_clk
        if hasattr(response, "clk"):
            self._clk = response.clk

    # Esa commands:
    def connect(self):
        try:
            conn = socket.create_connection((self._host, self._port))
            if self._port == 443:
                conn = ssl.wrap_socket(conn)
            self._conn = conn
            self._start_recv()

            # wait until connection is established
            while not self._connection_id:
                sleep(1)
        except socket.error as e:
            logging.error("Error when connecting: %s" % e)
            exit(1)

    def authenticate(self):
        self._send_request(Authentication(self._app_key, self._session_manager.get_session()))

    def heartbeat(self):
        self._send_request(Heartbeat())

    def subscribe(self):
        subscription = Subscription()
        subscription.market_filter = self._market_filter

        if self._initial_clk and self._clk:
            logging.info("Resubscribing with initial clk {} and clk {}".format(self._initial_clk, self._clk))
            subscription.initial_clk = self._initial_clk
            subscription.clk = self._clk

        self._send_request(subscription)

    def disconnect(self):
        logging.info("Disconnecting...")
        self._close_socket()

    def terminate(self):
        if self._conn:
            self._close_socket()
        self._working = False
        logging.info("Terminated")

    def print_cache(self):
        logging.info(format_json(self._cache))

    @property
    def cache(self):
        return self._cache

import json
import logging
import socket
import ssl
import threading
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


class EsaClient:
    def __init__(self, host: str, port: int, app_key: str, session_token: str, heartbeat_interval_second: int):
        self._host = host
        self._port = int(port)
        self._app_key = app_key
        self._session_token = session_token
        self._heartbeat_interval_second = heartbeat_interval_second

        self._cache = Cache()
        self._conn = None
        self._connection_id = None
        self._initial_clk = None
        self._clk = None
        self._market_filter = MarketFilter()

    def init(self):
        logging.info('Initialising ESA client')
        self._connect_and_auth()
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

        while True:
            try:
                while self._conn:
                    self.heartbeat()
                    sleep(self._heartbeat_interval_second)

                logging.info("Stopped sending.")
                self._reconnect_and_auth()
            except KeyboardInterrupt:
                logging.warning("KeyboardInterrupt.  Exiting...")

                self._stop_recv_threads()
                while self._recv_thread.is_alive():
                    sleep(1)

                exit(1)

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
            logging.error(e)

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
            logging.warning("Connection closed.")
            self._stop_recv_threads()

    def _receive_requests(self):
        while self._conn:
            self._receive_request()

        logging.info("Stopped receiving.")

    def _receive_request(self):
        message = self._recv()
        if message:
            self._process_response(message)

    def _send_request(self, request: Request):
        if request:
            message = serialise(request)
            logging.info("Sending: %s", message)
            self._send(message)

    def _process_response(self, message: dict):
        op = message["op"]

        if op == "connection":
            response = Connection(message)
            self._connection_id = response.connection_id
            logging.info("Connection has been established with ID %s", self._connection_id)
        elif op == "status":
            response = Status(message)
            logging.info("Received: %s", response)

            if response.connection_closed:
                self._stop_recv_threads()

        elif op == "mcm":
            response = MarketChangeMessage(message)

            self._update_clk(response)

            if hasattr(response, "mc"):
                self._cache.on_receive(response.mc)
                logging.info(self._cache.formatted_string())

        else:
            logging.error("Unknown message received.")

    def _update_clk(self, response: MarketChangeMessage):
        if hasattr(response, "_initial_clk"):
            self._initial_clk = response.initial_clk
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
            logging.error(e)
            exit(1)

    def authenticate(self):
        self._send_request(Authentication(self._app_key, self._session_token))

    def heartbeat(self):
        self._send_request(Heartbeat())

    def subscribe(self, params=list()):
        subscription = Subscription()
        subscription.market_filter = self._market_filter

        if isinstance(params, MarketFilter):
            self._market_filter = params
        else:
            if isinstance(params, list) and len(params) > 0:
                market_ids = params
            else:
                market_ids = []

            self._market_filter._market_ids = market_ids

        self._send_request(subscription)

    def resubscribe(self):
        subscription = Subscription()
        subscription.initial_clk = self._initial_clk
        subscription.clk = self._clk
        subscription.market_filter = self._market_filter

        self._send_request(subscription)

    def disconnect(self):
        logging.info("Disconnecting...\n")
        self._close_socket()

    def terminate(self):
        if self._conn:
            self._close_socket()
        logging.info("Terminated.")
        exit(0)

    def print_cache(self):
        logging.info(format_json(self._cache))

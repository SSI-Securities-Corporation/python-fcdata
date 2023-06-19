import websocket
import threading
import requests
import traceback
import time
import ssl
from .reconnection import ConnectionStateChecker
from .connection import ConnectionState
from ..hubs.errors import HubError, HubConnectionError, UnAuthorizedHubError
from .base_transport import BaseTransport
from ..helpers import Helpers
from json import dumps, loads
from urllib.parse import urlparse, urlunparse, urlencode

class WebsocketTransport(BaseTransport):
    def __init__(self,
            url="",
            headers=None,
            keep_alive_interval=15,
            reconnection_handler=None,
            verify_ssl=False,
            skip_negotiation=False,
            enable_trace=False,
            **kwargs):
        super(WebsocketTransport, self).__init__(**kwargs)
        self.protocol_version = '1.5'
        self._ws = None
        self.enable_trace = enable_trace
        self._thread = None
        self.skip_negotiation = skip_negotiation
        self.url = url
        if headers is None:
            self.headers = dict()
        else:
            self.headers = headers
        self.handshake_received = False
        self.token = None  # auth
        self.state = ConnectionState.disconnected
        self.connection_alive = False
        self._thread = None
        self._ws = None
        self.verify_ssl = verify_ssl
        self.conn_data = ''
        self.connection_checker = ConnectionStateChecker(
            lambda: self.logger.debug("Ping"),
            keep_alive_interval
        )
        self.reconnection_handler = reconnection_handler

        if len(self.logger.handlers) > 0:
            websocket.enableTrace(self.enable_trace, self.logger.handlers[0])
    
    def is_running(self):
        return self.state != ConnectionState.disconnected

    def stop(self):
        if self.state == ConnectionState.connected:
            self.connection_checker.stop()
            self._ws.close()
            self.state = ConnectionState.disconnected
            self.handshake_received = False

    def start(self, connectionData = ''):
        self.conn_data = connectionData
        if not self.skip_negotiation:
            self._negotiate()

        if self.state == ConnectionState.connected:
            self.logger.warning("Already connected unable to start")
            return False

        self.state = ConnectionState.connecting
        self.logger.debug("start url:" + self.url)
        self._ws = websocket.WebSocketApp(
            self.url,
            header=self.headers,
            on_message=self.on_message,
            on_error=self.on_socket_error,
            on_close=self.on_close,
            on_open=self.on_open,
            )
            
        self._thread = threading.Thread(
            target=lambda: self._ws.run_forever(
                sslopt={"cert_reqs": ssl.CERT_NONE}
                if not self.verify_ssl else {}
            ))
        self._thread.daemon = True
        self._thread.start()
        return True

    @staticmethod
    def _format_url(url, action, query):
        return '{url}/{action}?{query}'.format(url=url, action=action, query=query)
    
    def _get_ws_url_from(self):
        parsed = urlparse(self.url)
        scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        url_data = (scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)

        return urlunparse(url_data)
    @staticmethod
    def _get_cookie_str(request):
        return '; '.join([
            '%s=%s' % (name, value)
            for name, value in request.items()
        ])
    def _get_socket_url(self, responseData):
        ws_url = self._get_ws_url_from()
        query = urlencode({
            'transport': 'webSockets',
            'connectionToken':responseData['ConnectionToken'],
            'connectionData': self.conn_data,
            'clientProtocol': responseData['ProtocolVersion'],
        })

        return self._format_url(ws_url, 'connect', query)
    def _negotiate(self):
        query = urlencode({
            'connectionData': self.conn_data,
            'clientProtocol': self.protocol_version,
        })
        negotiate_url = self._format_url(self.url, 'negotiate', query)
        self.logger.debug("Negotiate url:{0}".format(negotiate_url))

        response = requests.post(
            negotiate_url, headers=self.headers, verify=self.verify_ssl)
        self.logger.debug(
            "Response status code{0}".format(response.status_code))

        if response.status_code != 200:
            raise HubError(response.status_code)\
                if response.status_code != 401 else UnAuthorizedHubError()

        data = response.json()
        print(self.headers)
        # self.headers['Cookie'] = self._get_cookie_str(response.cookies)
        self.url = self._get_socket_url(data)

       

    def on_open(self, _):
        self.logger.debug("-- web socket open --")
        self._on_open()

    def on_close(self, callback, close_status_code, close_reason):
        self.logger.debug("-- web socket close --")
        self.logger.debug(close_status_code)
        self.logger.debug(close_reason)
        self.state = ConnectionState.disconnected
        if self._on_close is not None and callable(self._on_close):
            self._on_close()
        if callback is not None and callable(callback):
            callback()

    def on_reconnect(self):
        self.logger.debug("-- web socket reconnecting --")
        self.state = ConnectionState.disconnected
        if self._on_close is not None and callable(self._on_close):
            self._on_close()

    def on_socket_error(self, app, error):
        """
        Args:
            _: Required to support websocket-client version equal or greater than 0.58.0
            error ([type]): [description]

        Raises:
            HubError: [description]
        """
        self.logger.debug("-- web socket error --")
        self.logger.error(traceback.format_exc(10, True))
        self.logger.error("{0} {1}".format(self, error))
        self.logger.error("{0} {1}".format(error, type(error)))
        self._on_close()
        self.state = ConnectionState.disconnected
        #raise HubError(error)

    def on_message(self, app, raw_message):
        self.logger.debug("Message received{0}".format(raw_message))
        if len(raw_message) > 0:
            return self._on_message(raw_message)

    def send(self, message):
        self.logger.debug("Sending message {0}".format(message))
        try:
            self._ws.send(dumps(message))
            self.connection_checker.last_message = time.time()
            if self.reconnection_handler is not None:
                self.reconnection_handler.reset()
        except (
                websocket._exceptions.WebSocketConnectionClosedException,
                OSError) as ex:
            self.handshake_received = False
            self.logger.warning("Connection closed {0}".format(ex))
            self.state = ConnectionState.disconnected
            if self.reconnection_handler is None:
                if self._on_close is not None and\
                        callable(self._on_close):
                    self._on_close()
                raise ValueError(str(ex))
            # Connection closed
            self.handle_reconnect()
        except Exception as ex:
            raise ex

    def handle_reconnect(self):
        if not self.reconnection_handler.reconnecting and self._on_reconnect is not None and \
                callable(self._on_reconnect):
            self._on_reconnect()
        self.reconnection_handler.reconnecting = True
        try:
            self.stop()
            self.start()
        except Exception as ex:
            self.logger.error(ex)
            sleep_time = self.reconnection_handler.next()
            threading.Thread(
                target=self.deferred_reconnect,
                args=(sleep_time,)
            ).start()

    def deferred_reconnect(self, sleep_time):
        time.sleep(sleep_time)
        
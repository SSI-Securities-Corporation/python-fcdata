import json
from .signalr import Connection
from .model import api
from .model import constants
from .fc_md_client import MarketDataClient


class MarketDataStream(object):

  def __init__(self, _config, client: MarketDataClient, on_close=None, on_open=None):

    self._config = _config
    self._client = client
    self._handlers = []
    self._error_handlers = []
    self._on_open = on_open
    self._on_close = on_close


  def _on_message(self, _message):
    x = json.loads(_message)
    try:
      for _handler in self._handlers:
        _handler(x)
    except:
      raise Exception(constants.RECEIVE_ERROR_MESSAGE)

  def on_close(self):
      if self._on_close and callable(self._on_close):
        self._on_close()

  def on_open(self):
    if self._on_open and callable(self._on_open):
      self._on_open()
  def _on_error(self, _error):

    _error = _error

    for _error_handler in self._error_handlers:

      _error_handler(_error)

  def swith_channel(self, channel):
    self.hub_proxy.server.invoke('SwitchChannels', channel)
     
  def start(self, _on_message, _on_error, _selected_channel, *argv):

    self._handlers.append(_on_message)
    self._channel = _selected_channel
    self._error_handlers.append(_on_error)
    headers = {}#utils.default_headers()
    using_jwt = self._client._get_access_token()
    headers['Authorization'] = self._config.auth_type \
          + constants.ONE_WHITE_SPACE + using_jwt
      
      
    self.connection = Connection(self._config.stream_url + api.SIGNALR, headers, on_close=self.on_close, on_open=self.on_open)
    
    self.hub_proxy = self.connection.register_hub(api.SIGNALR_HUB_MD)

    self.hub_proxy.client.on(api.SIGNALR_METHOD, self._on_message)

    self.hub_proxy.client.on(api.SIGNALR_ERROR_METHOD, self._on_error)
    
    self.connection.error += _on_error
    self.connection.on_open_callback(lambda: self.hub_proxy.server.invoke('SwitchChannels', _selected_channel))
    self.connection.start()
      
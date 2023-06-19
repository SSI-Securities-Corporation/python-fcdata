#!/usr/bin/python
# -*- coding: utf-8 -*-

# signalr_aio/_connection.py
# Stanislav Lazarov


from .events import EventHook
from .hubs import Hub
from .transports import WebsocketTransport
from .helpers import Helpers
from json import dumps, loads
import logging

class Connection(object):
    protocol_version = '1.5'

    def __init__(self, url, headers=None):
        self.url = url
        self.__hubs = {}
        self.__send_counter = -1
        self.hub = None
        self.session = None
        self.headers = headers
        self.received = EventHook()
        self.error = EventHook()
        self.started = False
        self.logger = Helpers.get_logger()
        self.__transport = WebsocketTransport(self.url, self.headers, on_message=self._on_message )
        
        def handle_error(**kwargs):
            error = kwargs["E"] if "E" in kwargs else None
            if error is None:
                return

            self.error.fire(error)

        self.received += handle_error

    def start(self):
        cdata = self._get_conn_data(self.__hubs)
        self.logger.debug("Connection started")
        return self.__transport.start(connectionData=cdata)
    @staticmethod
    def _get_conn_data(hubs):
        conn_data = dumps([{'name': hub for hub in hubs}])
        return conn_data
    
    def on_open_callback(self, callback):
        self.__transport.on_open_callback(callback=callback)
    
    def _on_message(self, data):
        msg = loads(data)
        self.received.fire(**msg)
    
    def on_open(self, data):
        msg = loads(data)
        self.received.fire(**msg)
        
    def register_hub(self, name):
        if name not in self.__hubs:
            if self.started:
                raise RuntimeError(
                    'Cannot create new hub because connection is already started.')
            self.__hubs[name] = Hub(name, self)
            return self.__hubs[name]

    def increment_send_counter(self):
        self.__send_counter += 1
        return self.__send_counter

    def send(self, message):
        self.__transport.send(message)

    def close(self):
        self.__transport.close()

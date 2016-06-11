from .core import BaseComponent, BaseEvent
from .net import TCPNetworkServer, UDPNetworkServer, UDPNetworkClient, TCPNetworkClient

import requests
import logging

class NetworkProducer(BaseComponent):
    producer = True
    TCP = 'tcp'
    UDP = 'udp'

    def configure(self, protocol=TCP, host='127.0.0.1', port=None):
        if protocol == self.TCP:
            self.ServerClass = TCPNetworkServer
        elif protocol == self.UDP:
            self.ServerClass = UDPNetworkServer
        self.host = host
        self.port = port

    def produce(self):
        server = self.ServerClass(self.process_data, self.host, self.port)
        server.listen()

    def process_data(self, client, payload):
        self.event({'client': client, 'payload': payload})

class NetworkConsumer(BaseComponent):
    def configure(self, protocol=TCP, host=None, port=None):
        if protocol == self.TCP:
            self.ClientClass = TCPNetworkServer
        elif protocol == self.UDP:
            self.ClientClass = UDPNetworkServer
        self.host = host
        self.port = port

    def consume(self):
        server = self.ClientClass(self.host, self.port)
        while True:
            event = self.queue.get()
            self.server

class TriggerWebhookConsumer(BaseComponent):
    pass

class ConsoleConsumer(BaseComponent):
    consumer = True

    def consume(self):
        while True:
            event = self.queue.get()
            print(event)

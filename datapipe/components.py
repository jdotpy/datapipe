from .core import BaseComponent

import requests
import socket

class NetworkSocket():
    TCP_PROTOCOL = 'tcp'
    UDP_PROTOCOL = 'udp'

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        self.protocol = kwargs.get('protocol', self.TCP_PROTOCOL)
        self.bind = kwargs.get('bind', False)
        self.receive_buffer = kwargs.get('receive_buffer', 1024)
        self.send_buffer = kwargs.get('send_buffer', 1024)
        self._create_socket()

    def listen(self):
        if not self.listener:
            raise ValueError('NetworkSocket not configured to listen.')

    def send(self):
        if not self.sender:
            raise ValueError('NetworkSocket not configured to send.')

    def _create_socket(self): 
        if self.protocol == self.TCP_PROTOCOL:
            socket_type = socket.SOCK_STREAM
            for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket_type):
                af, socktype, proto, canonname, sa = res
                try:
                    self._socket = socket.socket(af, socktype, proto)
                except OSError as e:
                    self._socket = None
                    continue
                try:
                    if self.bind:
                        self._socket.bind(sa)
                    else:
                        self._socket.connect(sa)
                except OSError as e:
                    s.close()
                    self._socket = None
                    continue
                break
        else:
            socket_type = socket.SOCK_DGRAM
            self._socket.socket(socket.AF_INET, socket_type)
            if self.bind:
                self._socket.bind((UDP_IP, UDP_PORT))
        return self._socket

class NetworkProducer(BaseComponent):
    pass

class NetworkConsumer(BaseComponent):
    pass

class WebhookConsumer(BaseComponent):
    pass

class LoggingConsumer(BaseComponent):
    pass

